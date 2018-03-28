import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { Subject } from 'rxjs/Subject';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

/**
 * Create and maintain a connection to the server. The connection runs over our
 * websocket with a custom protocol on top (defined in {@link payload}). All of
 * the events are replayed using our event emitters.
 *
 * Each thread within the payload can also be bound to giving components the
 * ability to listen for when a specific thread sends data and reading only
 * that data.
 */
@Injectable()
export class SocketService {

  // websocket handling parameters
  public url: string;
  private _socket: WebSocket;
  private _closeEvent: CloseEvent;
  private _receiveCallbacksQueue: Array<{ resolve: (data: any) => void, reject: (reason: any) => void }>;
  private _receiveDataQueue: Array<any>;

  // event handling parameters
  public onConnectionState: BehaviorSubject<number> = new BehaviorSubject(WebSocket.CLOSED);
  public onDataSent: Subject<number> = new Subject();
  public onDataReceived: Subject<number> = new Subject();

  // public onDataReceived: EventEmitter<boolean> = new EventEmitter();
  // public onDataError: EventEmitter<boolean> = new EventEmitter();
  // public onChannelReceived: Array<EventEmitter<boolean>>;

  /**
   * Constructor simply resets the data arrays and removes the close event from
   * being triggered. This is to ensure when a new instance is instantiated, we
   * dont confuse event listeners by telling it we have been disconnected.
   *
   * @returns void
   */
  public constructor() {
    this.url = environment.api;
    if (!this.connected) {
      this._reset();
      this.connect();
    }
  }

  /**
   * Check if the connection to the server exists, is connected and the socket
   * returns a state of {@link Websocket.OPEN}. If all is defined and connected
   * return true. Checking != null also checks against undefined.
   *
   * @returns true if the connection exists and is open.
   */
  public get connected(): boolean {
    return this._socket != null && this._socket.readyState === WebSocket.OPEN;
  }

  /**
   * The number of messages available to receive.
   *
   * @returns The number of queued messages that can be retrieved with {@link #receive}
   */
  public get dataAvailable(): number {
    return this._receiveDataQueue.length;
  }

  /**
   * Sets up a WebSocket connection to specified url. Resolves when the
   * connection is established. Can be called again to reconnect to any url.
   */
  public connect(url?: string, protocols?: string): Promise<void> {
    // if a url is provided, use it, else use the environments url
    url = url ? url : this.url;

    return this.disconnect().then(() => {
      this._reset();

      this._socket = new WebSocket(url, protocols);
      this._socket.binaryType = 'arraybuffer';
      this.onConnectionState.next(this._socket.readyState);
      return this._setupListenersOnConnect();
    });
  }

  /**
   * Send data through the websocket.
   * Must be connected. See {@link #connected}.
   */
  public send(data: string): void {
    if (!this.connected) {
      this.onConnectionState.next(this._socket.readyState);
      throw this._closeEvent || new Error('Not connected.');
    }

    this._socket.send(data);
    this.onDataSent.next(data.length);
  }

  /**
   * Asynchronously receive data from the websocket.
   * Resolves immediately if there is buffered, unreceived data.
   * Otherwise, resolves with the next rececived message,
   * or rejects if disconnected.
   *
   * @returns A promise that resolves with the data received.
   */
  public receive(): Promise<any> {
    if (this._receiveDataQueue.length !== 0) {
      return Promise.resolve(this._receiveDataQueue.shift());
    }

    if (!this.connected) {
      this.onConnectionState.next(this._socket.readyState);
      return Promise.reject(this._closeEvent || new Error('Not connected.'));
    }

    const receivePromise: Promise<any> = new Promise((resolve, reject) => {
      this._receiveCallbacksQueue.push({ resolve, reject });
    });

    return receivePromise;
  }

  /**
   * Initiates the close handshake if there is an active connection.
   * Returns a promise that will never reject.
   * The promise resolves once the WebSocket connection is closed.
   *
   * FIXME: Removed ? before CloseEvent
   */
  public disconnect(code?: number, reason?: string): Promise<CloseEvent> {
    if (!this.connected) {
      // this.onConnectionState.next(this._socket.readyState);
      return Promise.resolve(this._closeEvent);
    }

    return new Promise((resolve, reject) => {
      // It's okay to call resolve/reject multiple times in a promise.
      const callbacks = {
        resolve: dummy => {
          // Make sure this object always stays in the queue
          // until callbacks.reject() (which is resolve) is called.
          this._receiveCallbacksQueue.push(callbacks);
        },

        reject: resolve
      };

      this._receiveCallbacksQueue.push(callbacks);
      // After this, we will imminently get a close event.
      // Therefore, this promise will resolve.
      this._socket.close(code, reason);
      this.onConnectionState.next(this._socket.readyState);
    });
  }

  /**
   * Sets up the event listeners, which do the bulk of the work.
   *
   * @private
   */
  private _setupListenersOnConnect(): Promise<void> {
    const socket = this._socket;

    return new Promise((resolve, reject) => {

      const handleMessage: EventListener = event => {
        this.onDataReceived.next(event['data'].length);
        if (this._receiveCallbacksQueue.length !== 0) {
          this._receiveCallbacksQueue.shift().resolve(event['data']);
          return;
        }
        this._receiveDataQueue.push(event['data']);
      };

      // const handleMessage: EventListener = event => {
      //   console.log(event);
      //   const messageEvent: MessageEvent = ((event: any): MessageEvent);
      //   // The cast was necessary because Flow's libdef's don't contain
      //   // a MessageEventListener definition.

      //   if (this._receiveCallbacksQueue.length !== 0) {
      //     this._receiveCallbacksQueue.shift().resolve(messageEvent.data);
      //     return;
      //   }

      //   this._receiveDataQueue.push(messageEvent.data);
      // };

      const handleOpen: EventListener = event => {
        this.onConnectionState.next(this._socket.readyState);
        socket.addEventListener('message', handleMessage);
        socket.addEventListener('close', c_event => {
          // this._closeEvent = ((c_event: any): CloseEvent);
          this._closeEvent = c_event;

          // Whenever a close event fires, the socket is effectively dead.
          // It's impossible for more messages to arrive.
          // If there are any promises waiting for messages, reject them.
          while (this._receiveCallbacksQueue.length !== 0) {
            this._receiveCallbacksQueue.shift().reject(this._closeEvent);
          }
        });
        resolve();
      };

      socket.addEventListener('error', reject);
      socket.addEventListener('open', handleOpen);
    });
  }

  /**
   * @private
   */
  private _reset(): void {
    this._receiveDataQueue = [];
    this._receiveCallbacksQueue = [];
    this._closeEvent = null;
  }
}

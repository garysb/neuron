import { SocketService } from './socket.service';
import { Payload } from './payload';

export class SocketComponent {

  public constructor(protected socket: SocketService) {

    // subscribe to our connection state BehavourSubject
    this.socket.onConnectionState.subscribe({
      next: x => this.srvOnConnectionState(x),
      error: err => this.srvOnError(err),
      complete: () => console.log('Observer got a complete notification'),
    });

    // subscribe to data received Subject
    this.socket.onDataReceived.subscribe({
      next: x => this.srvOnDataReceived(x),
      error: err => this.srvOnError(err),
      complete: () => console.log('Observer got a complete notification'),
    });

    // subscribe to data sent Subject
    this.socket.onDataSent.subscribe({
      next: x => this.srvOnDataSent(x),
      error: err => this.srvOnError(err),
      complete: () => console.log('Observer got a complete notification'),
    });
  }

  protected srvOnConnectionState(state: number): void { }

  protected srvOnError(err: any): void {
    console.error('Error: ', err);
  }

  /**
   * When data is sent to the server, the Rxjs.Subject gets triggered with the
   * total size of the data send in bytes as its size value.
   */
  protected srvOnDataSent(size: number): void { }

  /**
   * When data is sent to the server, the Rxjs.Subject gets triggered with the
   * total size of the data send in bytes as its size value.
   */
  protected srvOnDataReceived(size: number): void { }
}

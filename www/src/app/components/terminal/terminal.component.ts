import { Component, OnInit } from '@angular/core';
import { SocketComponent } from '../../socket-component';
import { SocketService } from '../../socket.service';
import { Payload } from '../../payload';

@Component({
  selector: 'www-terminal',
  templateUrl: './terminal.component.html',
  styleUrls: ['./terminal.component.scss']
})
export class TerminalComponent extends SocketComponent implements OnInit {
  public snackbar: any;
  private model: Payload = new Payload('thread', 'action', 100, 0);
  public submitted: Boolean = false;
  public poll: Boolean = true;
  public threads: Array<String> = ['server', 'system.interface', 'system.threader', 'system.queue'];
  public incoming: Array<String> = new Array('Listening for messages');

  constructor(protected socket: SocketService) {
    super(socket);
  }

  private onClose() {
    this.snackbar.dismiss();
  }

  public onSubmit() {
    this.submitted = true;
    this.socket.send(JSON.stringify(this.model));
  }

  public ngOnInit() {
    this.onPoll();
  }

  private delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private async onPoll() {
    while (this.poll) {
      if (this.socket.dataAvailable !== 0) {
        this.onReceived(await this.socket.receive());
      }
      await this.delay(300);
    }
  }

  public onReceived(value) {
    this.incoming.push(value);
    console.log('incoming');
  }
}

import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatSnackBar, MatSnackBarRef } from '@angular/material';
import { SocketService } from '../../socket.service';
import { SocketComponent } from '../../socket-component';
import { TerminalComponent } from '../../components/terminal/terminal.component';

@Component({
  selector: 'layout-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent extends SocketComponent {
  private terminal: MatSnackBarRef<TerminalComponent>;
  protected connectionColor: String = 'red';
  protected uploadColor: String = 'gainsboro';
  protected downloadColor: String = 'gainsboro';

  constructor(protected socket: SocketService, public snackBar: MatSnackBar) {
    super(socket);
  }

  protected srvOnConnectionState(state: number) {
    switch (state) {
      case WebSocket.CLOSED:
        this.connectionColor = 'red';
        break;

      case WebSocket.CLOSING:
        this.connectionColor = 'orange';
        break;

      case WebSocket.CONNECTING:
      this.connectionColor = 'orange';
        break;

      case WebSocket.OPEN:
      this.connectionColor = 'green';
        break;

      default:
      this.connectionColor = 'red';
        break;
    }
  }

  protected srvOnDataSent(size: number): void {
    this.uploadColor = 'green';
    setTimeout(() => { this.uploadColor = 'gainsboro'; }, 100);
  }
  protected srvOnDataReceived(size: number): void {
    this.downloadColor = 'green';
    setTimeout(() => { this.downloadColor = 'gainsboro'; }, 100);
  }

  public openTerminal(): void {
    this.terminal = this.snackBar.openFromComponent(TerminalComponent, {
      panelClass: 'terminal',
    });
    this.terminal.instance.snackbar = this.terminal;
  }
}

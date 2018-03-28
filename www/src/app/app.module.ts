import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { FormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { LayoutModule } from './layout/layout.module';

import { ServiceWorkerModule } from '@angular/service-worker';
import { AppComponent } from './app.component';
import { environment } from '../environments/environment';
import { SocketService } from './socket.service';
import {
  MatButtonModule,
  MatCheckboxModule,
  MatInputModule,
  MatSelectModule,
  MatListModule,
  MatIconModule,
  MatMenuModule,
  MatSnackBarModule,
  MatSidenavModule
} from '@angular/material';

import { SystemComponent } from './components/system/system.component';
import { ThreadComponent } from './components/thread/thread.component';
import { QueueComponent } from './components/queue/queue.component';
import { TerminalComponent } from './components/terminal/terminal.component';

@NgModule({
  declarations: [
    AppComponent,
    SystemComponent,
    ThreadComponent,
    QueueComponent,
    TerminalComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    FlexLayoutModule,
    LayoutModule,
    ServiceWorkerModule.register('/ngsw-worker.js', { enabled: environment.production }),
    MatButtonModule,
    MatCheckboxModule,
    MatInputModule,
    MatSelectModule,
    MatListModule,
    MatIconModule,
    MatMenuModule,
    MatSnackBarModule,
    MatSidenavModule
  ],
  exports: [
    TerminalComponent
  ],
  providers: [
    SocketService
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }

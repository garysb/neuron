import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HeaderComponent } from './layout/header/header.component';
import { FooterComponent } from './layout/footer/footer.component';
import { NavigationComponent } from './layout/navigation/navigation.component';

import { SystemComponent } from './components/system/system.component';
import { ThreadComponent } from './components/thread/thread.component';
import { QueueComponent } from './components/queue/queue.component';

const routes: Routes = [
  { path: '', redirectTo: 'system', pathMatch: 'full' },
  { path: '', component: HeaderComponent },
  { path: '', component: FooterComponent },
  { path: '', component: NavigationComponent },
  { path: 'system', component: SystemComponent },
  { path: 'thread', component: ThreadComponent },
  { path: 'queue', component: QueueComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

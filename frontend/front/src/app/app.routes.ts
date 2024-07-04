import { Routes } from '@angular/router';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { LayoutComponent } from './components/layout/layout.component';
import { CrudComponent } from './components/crud/crud.component';
import { ReadComponent } from './components/read/read.component';
import { UpdateComponent } from './components/update/update.component';
import { LandminComponent } from './components/landmin/landmin.component';
import { AuthGuard } from './auth.service';
import { LandallComponent } from './components/landall/landall.component';
import { PictureComponent } from './components/picture/picture.component';

export const routes: Routes = [
  { path: 'register', component: RegisterComponent },
  { path: 'login',component:LoginComponent },
  { path:'landall',component:LandallComponent},
  { path: '', redirectTo: '/landall', pathMatch: 'full' },
  { path: 'crud', component: CrudComponent, canActivate: [AuthGuard]},
  { path: 'layout', component: LayoutComponent,canActivate:[AuthGuard] },
  { path:'read',component:ReadComponent,canActivate:[AuthGuard]},
  { path:'update/:id',component:UpdateComponent, canActivate:[AuthGuard]},
  { path:'landmin',component:LandminComponent,canActivate:[AuthGuard]},
  { path:'picture',component:PictureComponent},

];

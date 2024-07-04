import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { ApiService } from './service/api.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private apiService: ApiService, private router: Router) {}

  canActivate(): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {
      this.apiService.isAuthenticated().subscribe(
        (response) => {
          if (response.authenticated) {
            resolve(true);
          } else {
            this.router.navigate(['/login']); 
            resolve(false);
          }
        },
        (error) => {
          this.router.navigate(['/login']); 
          resolve(false);
        }
      );
    });
  }
}

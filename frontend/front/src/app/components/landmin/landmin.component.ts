import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../service/api.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-landmin',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './landmin.component.html',
  styleUrl: './landmin.component.css'
})
export class LandminComponent implements OnInit {
  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.apiService.isAuthenticated().subscribe(
      (response) => {
        if (!response.authenticated || response.username !== 'admin') {
          this.router.navigateByUrl('login');
        }
      },
      (error) => {
        console.error('Authentication check failed', error);
        this.router.navigateByUrl('login');
      }
    );
  }
  
  create():void{
    this.router.navigateByUrl('crud');

  }
  read():void{
    this.router.navigateByUrl('read');
  }
        
  logout(): void {
    this.apiService.logout().subscribe(
      response => {
        console.log('Logout successful', response);
        this.router.navigateByUrl('login'); 
      },
      error => {
        console.error('Logout failed', error);
      }
    );
  }

}

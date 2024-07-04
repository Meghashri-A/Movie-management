import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ApiService } from '../../service/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule,RouterModule]
})
export class LoginComponent implements OnInit {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {}

  onSubmit(): void {
    this.apiService.login(this.username, this.password).subscribe(
      (response: any) => {
        console.log(response);
        if (response.username === 'admin') {
          this.router.navigateByUrl('landmin');
        } else {
          this.router.navigateByUrl('layout');
        }
      },
      (error: any) => {
        console.error(error);
        if (error.status === 401) {
          if (error.error.detail === 'User not found') {
            this.errorMessage = 'User does not exist';
          } else if (error.error.detail === 'Incorrect password') {
            this.errorMessage = 'Incorrect password';
          } else {
            this.errorMessage = 'Unauthenticated! Please check your credentials.';
          }
        } else {
          this.errorMessage = error.error.message || 'An error occurred during login';
        }
      }
    );
  }

  onReset(): void {
    this.username = '';
    this.password = '';
    this.errorMessage = '';
  }
}

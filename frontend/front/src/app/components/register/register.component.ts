// register.component.ts

import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  standalone: true, 
  imports: [FormsModule, CommonModule] 
})
export class RegisterComponent {
  username: string = '';
  email: string = '';
  password: string = '';
  errorMessage: string = '';  

  constructor(private http: HttpClient, private router: Router) { }

  onSubmit() {
    const user = {
      "username": this.username,
      "password": this.password,
      "email": this.email
    };

    this.http.post('http://localhost:8000/zapp/register/', user)
      .subscribe(response => {
        console.log('User registered successfully', response);
        this.router.navigateByUrl('login');
      }, error => {
        console.error('Error registering user', error);
        if (error.status === 400 && error.error.message === 'User already exists') {
          this.errorMessage = 'User already exists';
        } else if (error.status === 400) {
          this.errorMessage = 'Invalid credentials';
        } else {
          this.errorMessage = 'An unexpected error occurred. Please try again later.';
        }
      });
  }
  onReset() {
    this.username = '';
    this.email = '';
    this.password = '';
    this.errorMessage = '';
  }
}
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../service/api.service'; // Adjust path as per your project structure
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-read-movies',
  templateUrl: './read.component.html',
  styleUrls: ['./read.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule],
})
export class ReadComponent implements OnInit {
  movies: any[] = [];
  errorMessage: string = '';

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.loadMovies();
  }

  loadMovies(): void {
    this.apiService.getMovies().subscribe(
      (data: any[]) => {
        this.movies = data;
        console.log(this.movies);
      },
      (error: any) => {
        console.error('Error loading movies', error);
        this.errorMessage = error.message;
      }
    );
  }
  

  deleteMovie(movieId: string): void {
    this.apiService.deleteMovie(movieId).subscribe(
      (response: any) => {
        console.log('Movie deleted successfully', response);
        this.movies = this.movies.filter((movie) => movie._id !== movieId);
      },
      (error: any) => {
        console.error('Error deleting movie', error);
        this.errorMessage = error.message;
      }
    );
  }

  editMovie(movieId: string): void {
    this.router.navigate(['/update', movieId]);
  }

  goBack(): void {
    this.router.navigate(['/landmin']);
  }
}
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../service/api.service'; // Adjust path as per your project structure
import { FormBuilder, FormGroup, FormsModule,ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-add-movie',
  templateUrl: './crud.component.html',
  styleUrls: ['./crud.component.css'],
  imports:[FormsModule,ReactiveFormsModule,CommonModule],
  standalone:true,
})
export class CrudComponent {
  movieName: string = '';
  yor: string = '';
  language: string = '';
  genre: string = '';
  description: string = '';
  castAndCrew: string = '';
  errorMessage: string = '';
  years: number[] = [];

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.populateYears();
  }

  populateYears() {
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 1900; year--) {
      this.years.push(year);
    }
  }

  onSubmit() {
    const movieData = {
      movie_name: this.movieName,
      yor: this.yor,
      language: this.language,
      genre: this.genre,
      description: this.description,
      cast_and_crew: this.castAndCrew
    };

    this.apiService.addMovie(movieData).subscribe(
      (response: any) => {
        console.log('Movie added successfully', response);
        this.router.navigateByUrl('/read'); 
      },
      (error: any) => {
        console.error('Error adding movie', error);
        this.errorMessage = error.error.message || 'An error occurred while adding the movie';
      }
    );
  }

  onReset() {
    this.movieName = '';
    this.yor = '';
    this.language = '';
    this.genre = '';
    this.description = '';
    this.castAndCrew = '';
    this.errorMessage = '';
  }
}
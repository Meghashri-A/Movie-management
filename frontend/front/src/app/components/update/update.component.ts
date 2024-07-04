import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../service/api.service'; // Adjust path as per your project structure
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-update',
  templateUrl: './update.component.html',
  styleUrls: ['./update.component.css'],
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, CommonModule],
})
export class UpdateComponent implements OnInit {
  movieId: string = '';
  movieName: string = '';
  yor: string = '';
  language: string = '';
  genre: string = '';
  description: string = '';
  castAndCrew: string = '';
  errorMessage: string = '';

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.movieId = this.route.snapshot.paramMap.get('id') || '';
    this.apiService.getMovieById(this.movieId).subscribe(
      (data: any) => {
        this.movieName = data.movie_name;
        this.yor = data.yor;
        this.language = data.language;
        this.genre = data.genre;
        this.description = data.description;
        this.castAndCrew = data.cast_and_crew;
      },
      error => {
        console.error(error);
        this.errorMessage = error.error.message;
      }
    );
  }

  onSubmit(): void {
    const movieData = {
      movie_name: this.movieName,
      yor: this.yor,
      language: this.language,
      genre: this.genre,
      description: this.description,
      cast_and_crew: this.castAndCrew
    };

    this.apiService.updateMovie(this.movieId, movieData).subscribe(
      response => {
        console.log(response);
        this.errorMessage = 'Movie updated successfully';
        this.router.navigate(['/read']);
      },
      error => {
        console.error(error);
        this.errorMessage = error.error.message || 'An error occurred while updating the movie';
      }
    );
  }
  
  goBack(): void {
    this.router.navigate(['/read']);
  }
}

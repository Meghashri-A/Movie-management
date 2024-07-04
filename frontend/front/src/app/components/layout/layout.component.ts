import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../service/api.service';
import { Observable, Subject, debounceTime, distinctUntilChanged, switchMap } from 'rxjs';

@Component({
  selector: 'app-add-movie',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.css'],
  imports:[FormsModule,ReactiveFormsModule,CommonModule],
  standalone:true,
})
export class LayoutComponent implements OnInit {
  movies: any[] = [];
  errorMessage: string = '';
  searchForm: FormGroup;
  searchTerms = new Subject<string>();

  constructor(
    private apiService: ApiService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {
    this.searchForm = this.formBuilder.group({
      query: [''],
      genre: [''],
      releaseYear: ['']
    });

    // Listen for search terms and trigger search
    this.searchTerms.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(term => this.searchMovies(term)),
    ).subscribe({
      next: (data: any[]) => {
        this.movies = data;
        this.errorMessage = '';
      },
      error: (err: any) => {
        console.error('Error searching movies', err);
        this.errorMessage = err.message || 'Error searching movies';
      }
    });
  }

  ngOnInit(): void {
    this.loadMovies();
  }

  loadMovies(): void {
    this.apiService.getMovies().subscribe(
      (data: any[]) => {
        this.movies = data;
      },
      (error: any) => {
        console.error('Error loading movies', error);
        this.errorMessage = error.message || 'Error loading movies';
      }
    );
  }

  searchMovies(query: string): Observable<any[]> {
    if (!query.trim()) {
      return this.apiService.getMovies(); 
    } else {
      return this.apiService.searchMovies(query);
    }
  }

  applyFilters(): void {
    const genre = this.searchForm.value.genre;
    const releaseYear = this.searchForm.value.releaseYear;

    this.apiService.filterMovies(genre).subscribe(
      (data: any[]) => {
        this.movies = data;
        this.errorMessage = '';
      },
      (error: any) => {
        console.error('Error filtering movies', error);
        this.errorMessage = error.message;
      }
    );
  }

  getPictureUrl(filename: string): string {
    return `http://localhost:8000/media/${filename}`; 
  }

  onSearchTermChanged(term: string): void {
    this.searchTerms.next(term);
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
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/zapp'; 

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const body = { username, password };
    return this.http.post(`${this.apiUrl}/login/`, body, { withCredentials: true });
  }
  
  isAuthenticated(): Observable<any> {
    return this.http.get(`${this.apiUrl}/isauthenticated/`, { withCredentials: true });
  }
  
  addMovie(movieData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/add/`, movieData, { withCredentials: true });
  }
  addMovieWithPicture(formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/add-movie/`, formData);
  }
  
  getMovies(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/read/`, { withCredentials: true });
  }

  getMovieById(movieId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/getmovbyid/${movieId}/`,{ withCredentials: true });
  }

  
  updateMovie(movieId: string, movieData: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/update/${movieId}/`, movieData, { withCredentials: true });
  }

  
  deleteMovie(movieId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${movieId}/`, { withCredentials: true });
  }
  
  searchMovies(query: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/search/?q=${query}`, { withCredentials: true });
  }

  
  filterMovies(genre: string): Observable<any[]> {
    let params = new HttpParams();
    if (genre) {
      params = params.append('genre', genre);
    }

    return this.http.get<any[]>(`${this.apiUrl}/filter/`, { params, withCredentials: true });
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout/`, {}, { withCredentials: true });
  }

  fetchImageNames(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/ret`);
  }

  uploadImage(imageFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('image', imageFile);

    return this.http.post<any>(`${this.apiUrl}/store`, formData);
  }
}

import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../service/api.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-picture',
  standalone: true,
  imports: [FormsModule,CommonModule,ReactiveFormsModule],
  templateUrl: './picture.component.html',
  styleUrl: './picture.component.css'
})
export class PictureComponent implements OnInit {

  selectedFile: File | null = null;
  previewImageUrl: string | ArrayBuffer | null = null;
  imageUrls: string[] = [];

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.loadImageUrls();
  }

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    if (file) {
      this.selectedFile = file;

      const reader = new FileReader();
      reader.onload = e => this.previewImageUrl = reader.result;
      reader.readAsDataURL(file);
    }
  }

  onSubmit(): void {
    if (this.selectedFile) {
      this.apiService.uploadImage(this.selectedFile).subscribe(
        (response) => {
          console.log('Image uploaded successfully', response);
          this.loadImageUrls(); // Reload image URLs after successful upload
        },
        (error) => {
          console.error('Error uploading image', error);
        }
      );
    }
  }

  loadImageUrls(): void {
    this.apiService.fetchImageNames().subscribe(
      (response) => {
        this.imageUrls = response.image_urls;
      },
      (error) => {
        console.error('Error retrieving image URLs', error);
      }
    );
  }
}
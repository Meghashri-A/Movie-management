import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landall',
  standalone: true,
  imports: [],
  templateUrl: './landall.component.html',
  styleUrl: './landall.component.css'
})
export class LandallComponent {
  constructor(private router:Router){}
    navigateTo(route:string):void
    {
         this.router.navigateByUrl(route);
    } 
  

}

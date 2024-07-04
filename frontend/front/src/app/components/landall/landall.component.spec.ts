import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LandallComponent } from './landall.component';

describe('LandallComponent', () => {
  let component: LandallComponent;
  let fixture: ComponentFixture<LandallComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LandallComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LandallComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

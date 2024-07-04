import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LandminComponent } from './landmin.component';

describe('LandminComponent', () => {
  let component: LandminComponent;
  let fixture: ComponentFixture<LandminComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LandminComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LandminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

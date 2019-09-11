/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { WordMeaningComponent } from './word-meaning.component';

describe('WordMeaningComponent', () => {
  let component: WordMeaningComponent;
  let fixture: ComponentFixture<WordMeaningComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WordMeaningComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WordMeaningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

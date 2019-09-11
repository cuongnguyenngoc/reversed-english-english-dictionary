/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { WordMeaningService } from './word-meaning.service';

describe('WordMeaningService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WordMeaningService]
    });
  });

  it('should ...', inject([WordMeaningService], (service: WordMeaningService) => {
    expect(service).toBeTruthy();
  }));
});

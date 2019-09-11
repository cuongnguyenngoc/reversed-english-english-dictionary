import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

@Injectable()
export class WordMeaningService {

  headers = new Headers();
  
  constructor(private http: Http) { 
    this.headers.append('Content-Type', 'application/json; charset=utf-8');
  }

  getMeaningOfWord(word) {
    console.log('fuck meaning', word);
    

    return this.http.post(
      'http://127.0.0.1:8000/api/dictionary/search/meaning/', 
      {word},
      this.headers
    ).map(res => res.json());
  }

  giveFeedbackToImproveSearchSystem(word, description) {
    console.log('hello new member', word, description);
    return this.http.post(
      'http://127.0.0.1:8000/api/dictionary/improve/receive-feedback/',
      {word, description},
      this.headers
    ).map(res => res.json());
  }

  crawlMeaningOfWord(word) {
    console.log('fuck meaning', word);

    return this.http.post(
      'http://127.0.0.1:8000/api/dictionary/search/meaning/', 
      {word},
      this.headers
    ).map(res => res.json());
  }
}

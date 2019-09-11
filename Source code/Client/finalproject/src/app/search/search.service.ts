import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/map';

@Injectable()
export class SearchService {

  constructor(private http: Http) { }

  getWords(method, description) {
    console.log('fuck', description);
    const headers = new Headers();
    headers.append('Content-Type', 'application/json; charset=utf-8');

    return this.http.post(
      'http://127.0.0.1:8000/api/dictionary/search/'+ method.replace(' ', '_').toLowerCase() +'/', 
      {description},
      headers
    ).map(res => res.json());
  }

}

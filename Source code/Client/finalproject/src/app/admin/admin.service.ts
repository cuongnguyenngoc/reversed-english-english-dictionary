import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions } from '@angular/http';

import { AuthService } from '../shared/auth/auth.service';

@Injectable()
export class AdminService {

  constructor(private http: Http, private authService: AuthService) { }

  getWordAndMeaningPairs() {
  	
    const headers = new Headers({ 'Authorization': 'JWT ' + this.authService.getToken() });
    headers.append('Content-Type', 'application/json; charset=utf-8');

    let options = new RequestOptions({ headers: headers });

    return this.http.get(
      'http://127.0.0.1:8000/api/admin/manage-word-defintion-pairs-from-users/', 
      options
    ).map(res => res.json());
  }

  approvePairOfWordAndMeaning(pair) {
    const headers = new Headers({ 'Authorization': 'JWT ' + this.authService.getToken() });
    headers.append('Content-Type', 'application/json; charset=utf-8');

    let options = new RequestOptions({ headers: headers });

    return this.http.post(
      'http://127.0.0.1:8000/api/admin/approve-word-defintion-pair-of-users/',
      {pair},
      options
    ).map(res => res.json());
  }

  crawlDictionary() {
    const headers = new Headers({ 'Authorization': 'JWT ' + this.authService.getToken() });
    headers.append('Content-Type', 'application/json; charset=utf-8');

    let options = new RequestOptions({ headers: headers });

    return this.http.get(
      'http://127.0.0.1:8000/api/dictionary/crawl/crawl-dictionary/', 
      options
    ).map(res => res.json());
  }

  updateSystem() {
    const headers = new Headers({ 'Authorization': 'JWT ' + this.authService.getToken() });
    headers.append('Content-Type', 'application/json; charset=utf-8');

    let options = new RequestOptions({ headers: headers });

    return this.http.get(
      'http://127.0.0.1:8000/api/dictionary/improve/updating-system/', 
      options
    ).map(res => res.json());
  }
}

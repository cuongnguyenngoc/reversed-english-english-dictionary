import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import { Router } from '@angular/router';

@Injectable()
export class AuthService {

  private token: String;
  private headers = new Headers();

  constructor(private router: Router, private http: Http) {
    this.headers.append('Content-Type', 'application/json;  charset=utf-8');
  }

  login(user) {

    return this.http.post(
      'http://127.0.0.1:8000/api/auth/token/', 
      user,
      this.headers
    )
    .map(
      res => {
        let token = res.json() && res.json().token;
        console.log(token);
        if (token) {
          // store username and jwt token in local storage to keep user logged in between page refreshes
          localStorage.setItem('currentUser', JSON.stringify({ user: user, token: token }));

          return true;
        }
        return false;
      }
    )
  }

  logout() {
    // clear token remove user from local storage to log user out
    localStorage.removeItem('currentUser');
    this.router.navigate(['/']);
  }

  getToken(): String {
    let currentUser = JSON.parse(localStorage.getItem('currentUser'));
    this.token = currentUser && currentUser.token;
    return this.token ? this.token : "";
  }

  isLoggedIn(): boolean {
    this.token = this.getToken();
    return this.token && this.token.length > 0;
  }

  getUser() {
    let currentUser = JSON.parse(localStorage.getItem('currentUser'));

    return currentUser && currentUser.user;
  }

  checkTokenExpired() {
    return this.http.post(
      'http://127.0.0.1:8000/api/auth/token-verify/',
      { 'token': this.token },
      this.headers
    ).map(res => res.json());
  }

}

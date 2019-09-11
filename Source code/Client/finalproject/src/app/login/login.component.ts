import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';

import { AuthService } from '../shared/auth/auth.service';
import { NotifyService } from '../shared/notify/notify.service';

declare const $: any;

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm = new FormGroup({
    username: new FormControl(),
    password: new FormControl()
  });

  constructor(private authService : AuthService, private notifyService : NotifyService) { }

  ngOnInit() {
  }

  onLogin() {
    console.log(this.loginForm.value);

    this.authService.login(this.loginForm.value).subscribe(
      data => {
        console.log(data);
        if (data) {
          $('#loginModal').modal('hide');
          this.notifyService.showNotification('Logged in successfully', 'pe-7s-check');
        }
      },
      err => {
        this.notifyService.showNotification('Your username or password is wrong', 'pe-7s-attention');
      }
    );
  }
}

import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  public sharedUrl = "http://localhost:4200/search";

  constructor(private authService: AuthService) { }

  ngOnInit() {
  }

  preventLoading(event) { event.preventDefault(); }

  logout(event) {
  	event.preventDefault();

  	this.authService.logout();
  }
}

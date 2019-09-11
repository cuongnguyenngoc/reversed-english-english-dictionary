import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { router } from './app.router';
import { CeiboShare } from 'ng2-social-share';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { SearchComponent } from './search/search.component';
import { ContentComponent } from './content/content.component';
import { FooterComponent } from './shared/footer/footer.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { LoginComponent } from './login/login.component';
import { WordMeaningComponent } from './search/word-meaning/word-meaning.component';

import { SearchService } from './search/search.service';
import { WordMeaningService } from './search/word-meaning/word-meaning.service';
import { AuthGuard } from './shared/auth/auth.guard';
import { AuthService } from './shared/auth/auth.service';
import { NotifyService } from './shared/notify/notify.service';
import { AdminComponent } from './admin/admin.component';
import { AdminService } from './admin/admin.service';
import { AdminCrawlerComponent } from './admin/admin-crawler/admin-crawler.component';
import { AdminApprovingComponent } from './admin/admin-approving/admin-approving.component';
import { AdminUpdateSystemComponent } from './admin/admin-update-system/admin-update-system.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SearchComponent,
    ContentComponent,
    FooterComponent,
    NavbarComponent,
    WordMeaningComponent,
    WordMeaningComponent,
    LoginComponent,
    AdminComponent,
    CeiboShare,
    AdminCrawlerComponent,
    AdminApprovingComponent,
    AdminUpdateSystemComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    router
  ],
  providers: [SearchService, WordMeaningService, AuthGuard, AuthService, NotifyService, AdminService],
  bootstrap: [AppComponent]
})
export class AppModule { }

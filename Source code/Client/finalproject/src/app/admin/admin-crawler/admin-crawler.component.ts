import { Component, OnInit } from '@angular/core';
import { AdminService } from '../admin.service';
import { NotifyService } from '../../shared/notify/notify.service';

@Component({
  selector: 'app-admin-crawler',
  templateUrl: './admin-crawler.component.html',
  styleUrls: ['./admin-crawler.component.scss']
})
export class AdminCrawlerComponent implements OnInit {

  private alert: boolean;
  private isLoading: boolean;

  constructor(private adminService: AdminService, private notifySerivce : NotifyService) { }

  ngOnInit() {
  }

  crawl() {
    this.alert = true;
    this.isLoading = true;

    this.adminService.crawlDictionary().subscribe(
      data => {
        this.alert = false;
        this.notifySerivce.showNotification(data.message, 'pe-7s-check');
        this.isLoading = false;
      },
      err => {
        this.notifySerivce.showNotification('Something went wrong', 'pe-7s-attention');
        this.isLoading = false;
      }
    );
  }
}

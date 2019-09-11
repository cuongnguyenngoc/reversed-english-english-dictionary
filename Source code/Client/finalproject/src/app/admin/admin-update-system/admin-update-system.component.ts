import { Component, OnInit } from '@angular/core';
import { AdminService } from '../admin.service';
import { NotifyService } from '../../shared/notify/notify.service';

@Component({
  selector: 'app-admin-update-system',
  templateUrl: './admin-update-system.component.html',
  styleUrls: ['./admin-update-system.component.scss']
})
export class AdminUpdateSystemComponent implements OnInit {

  private isLoading: boolean;

  constructor(private adminService: AdminService, private notifySerivce : NotifyService) { }

  ngOnInit() {
  }

  updateSystem() {
    this.isLoading = true;
    this.adminService.updateSystem().subscribe(
      data => {
        this.isLoading = false;
        this.notifySerivce.showNotification(data.message, 'pe-7s-check');
      },
      err => {
        this.notifySerivce.showNotification('Something went wrong', 'pe-7s-attention');
        this.isLoading = false;
      }
    )
  }

}

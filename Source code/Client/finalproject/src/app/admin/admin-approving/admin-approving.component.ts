import { Component, OnInit } from '@angular/core';
import { AdminService } from '../admin.service';
import { NotifyService } from '../../shared/notify/notify.service';

declare const $: any;

@Component({
  selector: 'app-admin-approving',
  templateUrl: './admin-approving.component.html',
  styleUrls: ['./admin-approving.component.scss']
})
export class AdminApprovingComponent implements OnInit {

  private wordAndMeaningPairs;

  constructor(private adminService: AdminService, private notifySerivce : NotifyService) { }

  ngOnInit() {
    this.adminService.getWordAndMeaningPairs().subscribe(
      data => {
        this.wordAndMeaningPairs = data;
        console.log(this.wordAndMeaningPairs);
      },
      err => {
        console.log(err);
      }
    );
  }

  approve(i) {
    this.wordAndMeaningPairs[i].isapproved = ($("#isapproved"+i).is(':checked')) ? true : false;
    console.log('this is approved ', this.wordAndMeaningPairs[i].isapproved)
  }

  saveApproving() {
    for (let pair of this.wordAndMeaningPairs) {
      if (pair.isapproved) {
        this.adminService.approvePairOfWordAndMeaning(pair).subscribe(
          data => {
            console.log(data);
            this.notifySerivce.showNotification(
              'Approving succeeded a pair word '+data.word.name+' and meaning '+data.def_field, 
              'pe-7s-check'
            );
            let index: number = this.wordAndMeaningPairs.indexOf(pair);
            if (index !== -1) {
              this.wordAndMeaningPairs.splice(index, 1);
            }
          },
          err => console.log(err)
        );
      }
    }
  }

}

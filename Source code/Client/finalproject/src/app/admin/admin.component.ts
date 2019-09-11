import { Component, OnInit } from '@angular/core';

declare const $: any;

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {

  private wordAndMeaningPairs;

  constructor() { }

  ngOnInit() {
    
  }

}

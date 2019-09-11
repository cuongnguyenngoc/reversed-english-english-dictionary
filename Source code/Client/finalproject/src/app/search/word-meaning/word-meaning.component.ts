import { Component, OnInit, Input, OnChanges, SimpleChanges, ElementRef } from '@angular/core';

import { WordMeaningService } from './word-meaning.service';
import { NotifyService } from '../../shared/notify/notify.service';

declare const $: any;

@Component({
  selector: 'app-word-meaning',
  templateUrl: './word-meaning.component.html',
  styleUrls: ['./word-meaning.component.scss']
})
export class WordMeaningComponent implements OnInit, OnChanges {

  @Input() word;
  @Input() description;

  private meaning: any;

  constructor(private wordMeaningService: WordMeaningService,
    private notifyService: NotifyService,
    private element: ElementRef) { }

  ngOnInit() {
  }

  ngOnChanges(changes: SimpleChanges) {
    console.log('changes', changes);
    this.meaning = null;

    this.wordMeaningService.getMeaningOfWord(this.word).subscribe(
      data => {
        if (data.message) {
          this.notifyService.showNotification(data.message, 'pe-7s-check');
        }
        this.meaning = data.word;
        console.log(this.meaning);
      },
      err => {
        console.log(err);
        this.notifyService.showNotification('Something went wrong', 'pe-7s-attention');
      }
    );
  }

  giveGoodFeedback() {
    this.wordMeaningService.giveFeedbackToImproveSearchSystem(this.word, this.description).subscribe(
      data => {
        console.log(data);
        this.notifyService.showNotification(data.message, 'pe-7s-check', '#myModal');
      }
    );
  }

  pronounce(i) {
    let pronounce = this.element.nativeElement.querySelector('#sound' + i);
    pronounce.play();
  }
}


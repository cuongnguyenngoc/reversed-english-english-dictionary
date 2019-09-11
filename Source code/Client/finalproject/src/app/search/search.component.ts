import {
  Component, 
  OnInit,
  trigger,
  state,
  style,
  animate,
  transition,
  ElementRef
} from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';

import { SearchService } from './search.service';
import { NotifyService } from '../shared/notify/notify.service';
import { WordMeaningService } from './word-meaning/word-meaning.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
  animations: [
    trigger('cardresults', [
      state('end', style({
        '-ms-transform': 'translate3D(0px, 0px, 0px)',
        '-webkit-transform': 'translate3D(0px, 0px, 0px)',
        '-moz-transform': 'translate3D(0px, 0px, 0px)',
        '-o-transform':'translate3D(0px, 0px, 0px)',
        transform:'translate3D(0px, 0px, 0px)',
        opacity: 5
      })),
      state('start', style({
        '-ms-transform': 'translate3D(0px, 150px, 0px)',
        '-webkit-transform': 'translate3D(0px, 150px, 0px)',
        '-moz-transform': 'translate3D(0px, 150px, 0px)',
        '-o-transform':'translate3D(0px, 150px, 0px)',
        transform:'translate3D(0px, 150px, 0px)',
        opacity: 0
      })),
      transition('start => end', [
        animate('0.3s 0.2s ease-out'),
      ])
    ])
  ]
})
export class SearchComponent implements OnInit {

  private methods;
  private method: String;
  private searchby: String;
  private searches;
  private description: String;
  private theBestWords;
  private state: String = 'start';
  private isLoading: boolean;
  private message: String;
  private word: String;
  private meaning;

  constructor(private searchService: SearchService, 
    private wordMeaningService: WordMeaningService,
    private notifyService: NotifyService,
    private element : ElementRef) {

  }

  ngOnInit() {
    this.method = 'Choose a method to search';
    this.methods = [
      'Basic Search',
      'Advanced Search'
    ];

    this.searchby = 'Choose search by word or description';
    this.searches = [
      'by word',
      'by description'
    ]
  }

  onSelectMethod(event, method) {
    event.preventDefault();

    this.method = method;
  }

  searchBy(event, search) {
    event.preventDefault();
    this.searchby = search;
  }

  search() {
    this.state = 'start';
    this.theBestWords = null;
    this.meaning = null;
    this.isLoading = true;

    if (this.searchby == this.searches[0]) {
      if (!this.searches.includes(this.searchby)) {
        this.searchby = this.searches[1];
      }

      this.wordMeaningService.getMeaningOfWord(this.description).subscribe(
        data => {
          if (data.message) {
            this.notifyService.showNotification(data.message, 'pe-7s-check');
          }
          this.meaning = data.word;
          console.log(this.meaning);
          this.state = 'end';
          this.isLoading = false;
        },
        err => {
          this.isLoading = false;
          this.notifyService.showNotification('Something went wrong. Please type another word', 'pe-7s-attention');
        }
      );
    } else {
      if (!this.methods.includes(this.method)) {
        this.method = this.methods[0];
      }

      this.searchService.getWords(this.method, this.description).subscribe(
        data => {
          this.theBestWords = data;
          console.log(this.theBestWords);
          this.state = 'end';
          this.isLoading = false;
        },
        err => {
          this.isLoading = false;
          this.notifyService.showNotification('Something went wrong. Please type another description', 'pe-7s-attention');
        }
      );
    }
  }

  showMeaningOfWord(word) {
    this.word = word;
  }

  pronounce(i) {
    let pronounce = this.element.nativeElement.querySelector('#sound' + i);
    pronounce.play();
  }
}

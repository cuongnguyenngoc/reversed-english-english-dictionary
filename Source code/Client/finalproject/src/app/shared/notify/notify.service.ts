import { Injectable } from '@angular/core';

declare const $: any;

@Injectable()
export class NotifyService {

  constructor() { }

  showNotification(message, icon, element='body') {
    $.notify({
      icon: icon,
      message: message
    },{
      element: element,
      allow_dismiss: true,
      type: 'danger',
      timer: 1000,
      placement: {
        from: 'bottom',
        align: 'center'
      }
    });
  }
}
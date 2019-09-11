import { FinalprojectPage } from './app.po';

describe('finalproject App', function() {
  let page: FinalprojectPage;

  beforeEach(() => {
    page = new FinalprojectPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});

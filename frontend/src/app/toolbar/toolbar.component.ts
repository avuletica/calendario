import {Component, OnInit} from '@angular/core';
import {NavigationStart, Router} from '@angular/router';

@Component({
    selector: 'app-toolbar',
    templateUrl: './toolbar.component.html',
    styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {
    loggedIn: boolean;

    // tslint:disable-next-line:variable-name
    constructor(private _router: Router) {
    }

    ngOnInit(): void {
        this._router.events.subscribe(event => {
            if (event instanceof NavigationStart) {
                this.loggedIn = localStorage.getItem('auth') != null;
            }
        });
    }

    onLogout(): void {
        localStorage.removeItem('auth');
        this.loggedIn = false;
    }

}

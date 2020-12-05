import {Component, OnInit} from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';

@Component({
    selector: 'app-registration',
    templateUrl: './registration.component.html',
    styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {
    hide = true;
    rootURL = 'http://localhost:8080';

    // tslint:disable-next-line:variable-name
    constructor(private _snackBar: MatSnackBar, private _http: HttpClient, private _router: Router) {
    }

    ngOnInit(): void {
    }

    onSubmit(data): void {
        this._http.post<any>(this.rootURL + '/api/v1/registration', data).subscribe(resp => {
                this._snackBar.open('Registration complete!', 'OK', {duration: 2000});
                this._router.navigateByUrl('/login');
            },
            error => {
                this._snackBar.open('Bad request', 'OK', {duration: 2000});
            }
        );
    }

}

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
                this.login(data);
            },
            error => {
                this._snackBar.open('Bad request', 'OK', {duration: 2000});
            }
        );
    }

    login(data): void {
        const formData: any = new FormData();
        formData.append('username', data.email);
        formData.append('password', data.password);
        this._http.post<any>(this.rootURL + '/api/v1/login/access-token', formData).subscribe(resp => {
                localStorage.setItem('auth', resp.access_token);
                this._router.navigateByUrl('/home');
                this._snackBar.open('Welcome ' + data.email, 'OK', {duration: 2000});
            },
            error => {
                this._snackBar.open(error.error.detail, 'OK', {duration: 2000});
            }
        );
    }

}

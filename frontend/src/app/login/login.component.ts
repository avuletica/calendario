import {Component} from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';

/** @title Input with a custom ErrorStateMatcher */
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  hide = true;

  // tslint:disable-next-line:variable-name
  constructor(private _snackBar: MatSnackBar, private _http: HttpClient, private _router: Router) {
  }


  onSubmit(data): void {
    if (!data.username || !data.password) {
      this._snackBar.open('Unauthorized', 'OK', {duration: 2000});
      return;
    }

    const formData: any = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);

    this._http.post<any>('http://calendario-be:8080/api/v1/login/access-token', formData).subscribe(resp => {
        localStorage.setItem('auth', resp.access_token);
        this._router.navigateByUrl('/home');
      },
      error => {
        this._snackBar.open(error.error.detail, 'OK', {duration: 2000});
      }
    );
  }


}

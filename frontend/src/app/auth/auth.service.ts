import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // tslint:disable-next-line:typedef
  isAuthenticated() {
    return localStorage.getItem('auth') != null;
  }
}

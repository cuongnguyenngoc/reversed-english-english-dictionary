import { Routes, RouterModule } from "@angular/router";

import { HomeComponent } from "./home/home.component";
import { SearchComponent } from "./search/search.component";
import { AdminComponent } from "./admin/admin.component";
import { AdminApprovingComponent } from "./admin/admin-approving/admin-approving.component";
import { AdminCrawlerComponent } from "./admin/admin-crawler/admin-crawler.component";
import { AdminUpdateSystemComponent } from "./admin/admin-update-system/admin-update-system.component";
import { AuthGuard } from "./shared/auth/auth.guard";

const APP_ROUTES: Routes = [
	{ path: '', redirectTo: '/home', pathMatch: 'full'},
	{ path: 'home', component: HomeComponent },
	{ path: 'search', component: SearchComponent},
	{ path: 'admin', redirectTo: '/admin/approving', pathMatch: 'full'},
	{ path: 'admin', component: AdminComponent, canActivate: [AuthGuard],
		children: [
			{ path: 'approving', component: AdminApprovingComponent, canActivate: [AuthGuard] },
			{ path: 'crawling', component: AdminCrawlerComponent, canActivate: [AuthGuard] },
			{ path: 'updating', component: AdminUpdateSystemComponent, canActivate: [AuthGuard] }
		]
	}
];

export const router = RouterModule.forRoot(APP_ROUTES);

import { h, Component } from 'preact';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser } from '@fortawesome/free-solid-svg-icons'
import style from './style';

export default class Home extends Component {

	state={
		filterMenuItemSelected: 0
	}

	filterMenuSelect(e){
		let listItems = document.getElementsByTagName("li");

		let menuItems = Object.values(this.listItems).filter((val, ind, arr)=>{
			if (val.style) {
				arr[ind].style.color="#486583";
				console.log(arr[ind]);
				return true;
			}
			arr[0].style.color="#7ab72d";
			return false;
		});
		

		menuItems.forEach(function(el,ind,arr){
			arr[ind].style.color="#486583";
			console.log(arr[ind])
			console.log(e.target)
			if (arr[ind] == e.target){
				e.target.style.color="#7ab72d";
				this.state.filterMenuItemSelected = ind;
			}
		});
	}

	render() {
		return (
			<div>
			<div class={style.titlebar}>hellokitty9009<div class={style.userIconBox}><FontAwesomeIcon icon={faUser} class={style.userIcon}/></div></div>
			<div class="flex-container">
			<div class={style.left}>
			<div class={style.filterMenu}>
			<ul class={style.nobullets} onClick={this.filterMenuSelect}>
			<li>Completed Modules</li>
			<li>Modules In-Progress</li>
			<li>Unlocked Modules Only</li>
			<li>All Unfinished Modules</li>
			</ul>
			</div>
			</div>
			<div class={style.right}>
			<div class={style.infobox}></div>
			</div>
			</div> 
			</div>
			);
		}
	}
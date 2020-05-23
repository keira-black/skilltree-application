import { h, Component } from 'preact';
import { Link } from 'preact-router/match';
import Card from 'preact-material-components/Card';
import 'preact-material-components/Card/style.css';
import 'preact-material-components/Button/style.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSignInAlt } from '@fortawesome/free-solid-svg-icons'
import style from './style';

export default class Register extends Component {
	render() {
		return (
			<div class={`${style.login} page`}>
				<div class={style.title}>SkillTree</div>
				<Card class={style.loginOutline}>
					<div class={style.cardBody}>
						<form>	
	  						<label class={style.loginLabel}>
	    						<div>
	    							username
	    						</div>
	    						<div class={style.loginDiv}>
	    							<input type="text" name="name" class={style.loginField}/>
	    						</div>
	  						</label>
	  						<label class={style.loginLabel}>
	  							<div>
	  								e-mail
	  							</div>
	  							<div>	
	  								<input type="text" name="email" class={style.loginField}/>
	  							</div>
	  						</label>	
	  						<button type="submit" class={style.submit}>
	  							<span class={style.submitButtonText}>
	  								register
	  							</span>
	  							<span class={style.submitIcon}>
	  								<FontAwesomeIcon icon={faSignInAlt}/>
	  							</span>
	  						</button>
	  						<div class={style.bottomText}>Or click <Link href="/login" class={style.registerLink}>here</Link> to login</div>
						</form>
					</div>
				</Card>
			</div>
		);
	}
}

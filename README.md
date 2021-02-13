# Automail

A badly written python bot that programmatically sends email replies to senders based of the contents of the email. Built for students responding to teachers. \
**Warning**: It's not a great idea to actually use this. This was just made for me to learn a little about the Gmail API and to have a little fun!

GitHub link [here](https://github.com/gadhagod/automail). You will probably need this to follow along with the rest of this post.

## How it works

Every ten minutes, it checks the latest email. If it is not sent by you or not in `config.json`.`ignore`, it reads the email and checks if it has certain keywords. For example, if the email has any of the following keywords/phrases:

* absent
* absence
* from class
* unexcused
* make up
* missed class
* not present
* attendance

It will be categorized as a "absent" email. There are five categories, chosen based off email the email's body's keywords. Then, it will start creating an email to reply with. It will start with the template in [absence.jinja](https://github.com/gadhagod/automail/blob/master/message_templates/absence.jinja), and will fill it in. The template looks like this:

    Hello M. {{ recipient }},  
    Thanks for your email. I was not able to attend because {{ excuse }}. I was meaning to tell you, but I completely forgot.  I am terribly sorry about all this.  
    {{ farewell }}, {{ me }} 

`recipient` is replaced with the email recipient, retrieved from the latest message.`excuse` is randomly chosen from `config.json`.`excuses`. `farewell` is configured in config.json. `me` is your name taken from the Gmail API. You can configure your excuses, farewell, and more by editing `config.json` .Using the Gmail API, it is sent in reply to the initial email.

A filled in template could look like this:

    Hello M. Green,  
    Thanks for your email. I was not able to attend because I had to rush my grandpa to the hospital, after a severely urgent incident. I was meaning to tell you, but I completely forgot.  
    I am terribly sorry about all this.  Have a great day, Aarav Borthakur 

That's it!

## Hosting it yourself

1. Follow [this tutorial](https://developers.google.com/youtube/v3/quickstart/python) to create your Google API project (free).
2. Run [setup.sh](https://github.com/gadhagod/automail/blob/master/setup.sh). It will direct you to an authorization page.
3. Make changes to [config.json](https://github.com/gadhagod/automail/blob/master/config.json). You can add office hours timings, farewells, and more.
4. Run [main.py](https://github.com/gadhagod/automail/blob/master/main.py) with `nohup source main.sh &`. This will keep it in the background of your machine. Errors are raised when the sender doesn't have a name, but these are not really "errors". 

## Disclaimer

Again, this project is not at all to be actually used. It's written pretty badly and not completely tested. I don't take responsibility for any suspensions, arrests, or other bad events. It's written in two days in crammed 10 minute school breaks. Don't expect much reliablity!
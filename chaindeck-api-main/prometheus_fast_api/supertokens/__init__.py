from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import emailpassword, session,jwt

init(
    app_info=InputAppInfo(
        app_name="test",
        api_domain="https://a5b968a6c7d3f4745a7bec16931a568b-1842195318.ap-south-1.elb.amazonaws.com:3567",
        website_domain="https://a5b968a6c7d3f4745a7bec16931a568b-1842195318.ap-south-1.elb.amazonaws.com",
        api_base_path="/auth",
        website_base_path="/auth"
    ),
    supertokens_config=SupertokensConfig(
        # https://try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
        connection_uri="https://a5b968a6c7d3f4745a7bec16931a568b-1842195318.ap-south-1.elb.amazonaws.com:3567",
        # api_key=<API_KEY(if configured)>
    ),
    framework='fastapi',
    recipe_list=[
        session.init(), # initializes session features
        emailpassword.init(),
        jwt.init()
    ],
    mode='asgi' # use wsgi if you are running using gunicorn
)
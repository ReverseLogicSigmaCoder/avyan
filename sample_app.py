
def handle_user_profile(user_id):
    # Potential IDOR / Unauthenticated Route
    cmd = request.args.get('cmd')
    os.system(cmd)  # Command Injection (Taint Sink)
    return db.query(User).filter_by(id=user_id).first()

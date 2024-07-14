class User:
    def __init__(self, id, db):
        self.id = id
        self.name = None
        self.email = None
        self.age = None
        self.gender = None
        self.genre = None

        self.getUser(db)

    def getUser(self,db):
        try:
            user = db.collection("userData").document(self.id).get()
            user = user.to_dict()
            self.id = user["id"]
            self.name = user["name"]
            self.email = user["email"]
            self.age = user["age"]
            self.gender = user["gender"]
            self.genre = user["genre"].split(",")
        except:
            pass

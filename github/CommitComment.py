from GithubObject import *

from NamedUser import NamedUser

CommitComment = GithubObject(
    "CommitComment",
    BaseUrl( lambda obj: obj._repo._baseUrl() + "/comments/" + str( obj.id ) ),
    InternalSimpleAttributes(
        "url", "id", "body", "path", "position", "commit_id",
        "created_at", "updated_at", "html_url", "line",
        "_repo",
    ),
    InternalObjectAttribute( "user", NamedUser ),
    Editable( [ "body" ], [] ),
    Deletable(),
)

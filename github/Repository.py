from GithubObject import *

from NamedUser import NamedUser
from Event import Event
from IssueEvent import IssueEvent
from RepositoryKey import RepositoryKey
from Hook import Hook
from GitBlob import GitBlob
from GitCommit import GitCommit
from GitRef import GitRef
from GitTag import GitTag
from GitTree import GitTree
from Label import Label
from Milestone import Milestone
from Issue import Issue
from Download import Download
from CommitComment import CommitComment
from Commit import Commit
from Tag import Tag
from Branch import Branch
from PullRequest import PullRequest

__modifyAttributesForObjectsReferingRepo = { "_repo": lambda repo: repo }

Repository = GithubObject(
    "Repository",
    BaseUrl( lambda obj: "/repos/" + obj.owner.login + "/" + obj.name ),
    Identity( lambda obj: obj.owner.login + "/" + obj.name ),
    InternalSimpleAttributes(
        "url", "html_url", "clone_url", "git_url", "ssh_url", "svn_url",
        "name", "description", "homepage", "language", "private",
        "fork", "forks", "watchers", "size", "master_branch", "open_issues",
        "pushed_at", "created_at", "organization",
        "has_issues", "has_wiki", "has_downloads",
        # Not documented
        "mirror_url", "updated_at", "id",
    ),
    InternalObjectAttribute( "owner", NamedUser ),
)
Repository._addAttributePolicy( InternalObjectAttribute( "parent", Repository ) )
Repository._addAttributePolicy( InternalObjectAttribute( "source", Repository ) )
Repository._addAttributePolicy(
    ExternalListOfObjects( "events", "event", Event,
        ListGetable( [], [] )
    ),
)
def __getNetworkEvents( repo ):
    return [
        Event( repo._github, attributes, lazy = True )
        for attributes
        in repo._github._dataRequest( "GET", "/networks/" + repo.owner.login + "/" + repo.name + "/events", None, None )
    ]
Repository._addAttributePolicy(
    MethodFromCallable( "get_network_events", [], [], __getNetworkEvents, SimpleTypePolicy( "list of `Event`" ) )
)
Repository._addAttributePolicy(
    ExternalListOfObjects( "issues/events", "issues_event", IssueEvent,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "id" ], [], __modifyAttributesForObjectsReferingRepo ),
    )
)
Repository._addAttributePolicy(
    ExternalListOfObjects( "forks", "fork", Repository,
        ListGetable( [], [] )
    )
)
Repository._addAttributePolicy(
    Editable( [ "name" ], [ "description", "homepage", "public", "has_issues", "has_wiki", "has_downloads" ] )
)
Repository._addAttributePolicy(
    SeveralAttributePolicies( [ ExternalSimpleAttribute( "languages", "dictionary of strings to integers" ) ], "Languages" )
)
Repository._addAttributePolicy( SeveralAttributePolicies( [
    ExternalListOfObjects( "hooks", "hook", Hook,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "id" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "name", "config" ], [ "events", "active" ], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "keys", "key", RepositoryKey,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "id" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "title", "key" ], [], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "collaborators", "collaborator", NamedUser,
        ListGetable( [], [] ),
        ElementAddable(),
        ElementRemovable(),
        ElementHasable()
    ),
    ExternalListOfObjects( "contributors", "contributor", NamedUser,
        ListGetable( [], [] )
    ),
    ExternalListOfObjects( "watchers", "watcher", NamedUser,
        ListGetable( [], [] )
    ),
    ExternalListOfObjects( "git/refs", "git_ref", GitRef,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "ref" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "ref", "sha" ], [], __modifyAttributesForObjectsReferingRepo )
    ),
    ExternalListOfObjects( "git/commits", "git_commit", GitCommit,
        ElementGetable( [ "sha" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "message", "tree", "parents" ], [ "author", "committer" ], __modifyAttributesForObjectsReferingRepo )
    ),
    ExternalListOfObjects( "git/trees", "git_tree", GitTree,
        ElementGetable( [ "sha" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "tree" ], [], __modifyAttributesForObjectsReferingRepo )
    ),
    ExternalListOfObjects( "git/blobs", "git_blob", GitBlob,
        ElementGetable( [ "sha" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "content", "encoding" ], [], __modifyAttributesForObjectsReferingRepo )
    ),
    ExternalListOfObjects( "git/tags", "git_tag", GitTag,
        ElementGetable( [ "sha" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "tag", "message", "object", "type" ], [ "tagger" ], __modifyAttributesForObjectsReferingRepo )
    ),
    ExternalListOfObjects( "labels", "label", Label,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "name" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "name", "color" ], [], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "milestones", "milestone", Milestone,
        ListGetable( [], [ "state", "sort", "direction" ], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "number" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "title" ], [ "state", "description", "due_on" ], __modifyAttributesForObjectsReferingRepo )
    ),
    ExternalListOfObjects( "issues", "issue", Issue,
        ListGetable( [], [ "milestone", "state", "assignee", "mentioned", "labels", "sort", "direction", "since" ], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "number" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "title" ], [ "body", "assignee", "milestone", "labels", ], __modifyAttributesForObjectsReferingRepo )
    ),
    ExternalListOfObjects( "downloads", "download", Download,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "id" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "name", "size" ], [ "description", "content_type" ], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "comments", "comment", CommitComment,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "id" ], [], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "commits", "commit", Commit,
        ListGetable( [], [ "sha", "path" ], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "sha" ], [], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "tags", "tag", Tag,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "branches", "branch", Branch,
        ListGetable( [], [], __modifyAttributesForObjectsReferingRepo ),
    ),
    ExternalListOfObjects( "pulls", "pull", PullRequest,
        ListGetable( [], [ "state" ], __modifyAttributesForObjectsReferingRepo ),
        ElementGetable( [ "number" ], [], __modifyAttributesForObjectsReferingRepo ),
        ElementCreatable( [ "title", "body", "base", "head" ], [], __modifyAttributesForObjectsReferingRepo ),
    ),
] ) )

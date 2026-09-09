# TidyBoard — Product Specification

## Purpose and audience

TidyBoard helps individuals organize personal work across multiple projects.
Each project has its own board. This project is a local, desktop-first online
workspace using an explicit development mock identity.

Google OAuth and external identity providers are removed from the product
design. This project makes no hosted privacy, account-isolation, or public
cross-device authentication claim.

This document defines product behavior only. The decisions below were agreed
during scope discussions; remaining minor assumptions are identified separately.

## First-release scope

- Development-only mock sign-in for local workflows. Hosted authentication and
  public cross-device workspaces are outside this project.
- Multiple named boards, ordered by most recently opened.
- Three fixed columns on every board: To Do, In Progress, and Done.
- Tasks with a required title and optional description.
- A side panel for viewing and editing tasks, with explicit Save and Cancel.
- Drag-and-drop movement between columns, plus a status selector for keyboard
  and mobile use. No manual ordering within a column.
- Board archiving and restoration. Archived boards remain editable.
- Permanent task deletion with confirmation.
- Search across all owned boards, including archived boards.
- Automatic updates across devices within about five seconds under normal
  connectivity, with protection against conflicting edits.
- Online use with unsaved text preserved when the connection drops.

## User journeys and behavior

### Sign in and access private work

A local user enters through the development mock session and sees a clear Create
board action. Returning local sessions can reopen the same configured SQLite
workspace; public multi-account access is outside this project.

People can sign out. A person must never be able to read, search, or change
another person's boards or tasks, including by opening a direct link.

### Create and find boards

A person creates a board by entering its name. Opening a board shows its three
fixed columns and makes it the most recently opened board in the active list.
Boards can be renamed. Renaming preserves all tasks and their statuses.

Active and archived boards have separate views. Archiving removes a board from
the active list without deleting it or its tasks. The archived view offers an
action to restore a board. Opening or editing an archived board does not restore
it automatically; it retains a visible Archived label.

Archived boards support the same task actions as active boards, including
creation, editing, movement, and deletion. Permanent board deletion is outside
the first release.

### Create a task

From an open board, a person chooses Add task and enters a title. A description
is optional. Saving creates the task in To Do and shows it on the board.
Canceling creates nothing. Creation in other columns is not offered.

### View and edit a task

Selecting a task opens a side panel while the board remains visible. The panel
contains the task title, description, status selector, Save, Cancel, and Delete.

Title and description edits remain drafts until Save succeeds. Cancel discards
the draft. Closing the panel or navigating away with unsaved edits asks whether
to discard them. A failed save leaves the draft available for correction or retry.

### Move a task

A person drags a task into another column or chooses its destination in the
status selector. All transitions are allowed, including returning a Done task
to To Do or In Progress. A selector change is saved with the panel's Save action;
a drag-and-drop move is saved immediately.

Tasks are ordered by creation time within their current column. Moving or editing
a task does not change its creation time. Dropping at a particular position does
not set its order. Completing a task keeps it visible in Done until deleted.

### Delete a task

Delete asks for confirmation and explains that deletion is permanent. Canceling
leaves the task unchanged. Confirming removes the task from its board and search
results only after deletion succeeds. There is no task archive or undo feature.

### Search the workspace

A person searches task titles and descriptions across all their boards. Results
include matching tasks from archived boards without requiring a toggle. Each
result identifies the task, board, and status; archived boards have a visible
Archived label. Selecting a result opens the correct board and task side panel.

No matches produces a clear empty result state. Search never includes another
person's content. Board-name search is outside the first release.

### Continue work across devices

While the tool is open and connected, changes saved on another device appear
within about five seconds under normal conditions. This includes board changes
and task creation, edits, movement, and deletion. Reloading also shows saved work.

Automatic updates must not replace an unsaved draft. If a task changes after a
person starts editing, saving the stale draft must not silently overwrite the
newer version. Show a conflict notice, retain the draft, and let the person review
the latest saved task before deliberately reapplying and saving their edits.

If the task was deleted elsewhere, explain that it no longer exists, retain any
draft text for copying, and prevent a save from silently recreating the task.

### Handle connection loss

The tool requires an internet connection. If connectivity drops, show an
offline or connection-error notice and keep unsaved text visible. Do not report
a save as successful until it is confirmed. Once connected, the person can retry.
The first release does not queue offline changes or promise draft recovery after
closing or reloading the browser.

## Visible states

- Loading: distinguish loading content from an empty board or empty search.
- Empty workspace: explain how to create the first board.
- Empty column: show its name and a brief empty-state message.
- Empty archive or search: explain that there are no matching items.
- Saving: indicate work in progress and prevent duplicate submissions.
- Success: reflect confirmed changes and provide clear save or action feedback.
- Validation error: identify the field and retain the entered content.
- Request failure: explain that the action failed and offer a retry where useful.
- Conflict: preserve the draft and offer review of the newer saved task.
- Sign-in failure or expired session: explain the need to sign in again without
  showing another person's data or claiming unsaved changes were saved.
- Unavailable item: explain when a board or task cannot be accessed or no longer
  exists; do not disclose private details about another person's content.

## Domain and lifecycle rules

| Item | Product rules |
| --- | --- |
| Workspace | Belongs to one signed-in person; contains only their boards. |
| Board | Has a name, an owner, an active/archived state, and the fixed columns. |
| Task | Belongs to exactly one board; has a title, description, creation time, and status. |
| Status | Exactly To Do, In Progress, or Done; new tasks start in To Do. |
| Archive | Reversible board state; preserves content and permits editing. |
| Deletion | Confirmed permanent removal of a task. |

Saved work must survive signing out, refreshing, closing the browser, and
restarting the service. Board and task ownership cannot be reassigned in the
first release. Tasks cannot be moved between boards.

## Acceptance criteria

1. A local user can enter through the mock sign-in, create two boards, and
   maintain separate task lists on them. External authentication, public
   cross-account privacy, and hosted access are outside this project.
2. Opening a board puts it first in the recently opened active-board list.
   Renaming a board preserves its tasks.
3. Every board has exactly To Do, In Progress, and Done; users cannot add,
   rename, reorder, or remove these columns.
4. A task can be created with a title alone and appears in To Do. Blank titles
   are rejected, and canceling creation leaves the board unchanged.
5. Opening a task shows its side panel. Saving title or description edits makes
   them persist; Cancel leaves the saved task unchanged. Leaving a dirty panel
   requires a discard decision.
6. Dragging a task or saving a status selection moves it to any chosen column.
   A failed move does not leave the task displayed as successfully moved.
7. Tasks retain creation-time ordering after edits and moves; dragging within
   a column cannot establish a custom order.
8. A task remains in Done until moved or deleted. Deletion requires confirmation;
   canceling preserves it, and successful deletion removes it from search.
9. Archiving a board removes it from the active list and places it in the archive.
   Its tasks remain fully editable. Restoring returns it to the active list.
10. Search finds matching title or description text across multiple owned boards,
    including archived boards. Results show board, status, and archive state,
    and open the selected task. An unmatched query shows a no-results state.
11. A second connected device sees confirmed changes within about five seconds
    under normal conditions without a manual refresh.
12. If two devices edit the same task, saving the stale draft produces a conflict
    notice rather than overwriting newer work, and the draft remains available.
    Remote deletion does not discard draft text or recreate the deleted task.
13. During connection loss, failed saves retain entered text and show an error.
    The user can retry after reconnection; no automatic offline queue is implied.
14. Boards, tasks, statuses, and archive state remain after browser and service
    restarts and are available when the same person signs in on another device.
15. Core actions work with a keyboard, including opening task details and moving
    tasks without dragging. Fields have labels, focus is visible, and status and
    errors do not rely on color alone.
16. A desktop workspace with 20 boards and 200 tasks per board remains usable:
    content is reachable, long text does not break the layout, and loading or
    saving states provide feedback. These are usability targets, not hard limits.

## Assumptions for review

These minor defaults were not explicitly selected during brainstorming:

- Board names and task titles are trimmed, required, and limited to 120 characters.
  Descriptions are optional plain text, limited to 5,000 characters. Invalid input
  is rejected with an explanation, never silently truncated.
- Duplicate board names and task titles are allowed; identity does not depend
  on the display name.
- Tasks appear oldest first within each column. Ordering remains stable when
  creation times tie.
- A newly created or restored board opens immediately. Recently opened order is
  shared across devices; archived boards also use most-recently-opened order.
- Search uses a case-insensitive substring match against title or description.
  Leading and trailing query whitespace is ignored. An empty query prompts for
  text; results are newest-created first and can be traversed if numerous.
- Automatic refresh preserves the open panel and draft. Review of a conflict
  presents both the draft and latest saved content; it never forces a blind
  overwrite.
- Initial support targets current desktop Chrome, Firefox, Edge, and Safari.
  Basic narrow-screen access should remain possible, but polished mobile layouts
  and mobile drag-and-drop are deferred.

## Explicit non-goals

- Shared boards, invitations, task assignments, team roles, and public links.
- Custom columns, task ordering, and movement between boards.
- Priorities, due dates, labels, checklists, attachments, comments, and rich text.
- Notifications, reminders, activity history, and analytics.
- Task archiving, deletion undo, and permanent board deletion.
- Offline editing, background synchronization of offline changes, and guaranteed
  draft recovery after browser closure.
- Instant live collaboration; the agreed update interval is about five seconds.
- Native mobile apps and a polished mobile-first experience.
- External authentication, imports, exports, and third-party integrations.

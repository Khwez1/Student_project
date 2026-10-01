# Activity: Documentation & Testing on the Student API

## Before You Start

This activity assumes your `student_app` already has a working `Student`
model, `StudentSerializer`, `IsOwnerOrReadOnly` permission, and
`StudentViewSet` — everything built across earlier sessions this module.
You're not adding new API behaviour today. You're documenting it, exploring
it manually, and proving it works automatically.

Three named cases, used throughout this whole activity:

| Case | What it checks |
|---|---|
| **DOC-001** | Listing students succeeds |
| **DOC-002** | An invalid mark is genuinely rejected |
| **DOC-003** | You can't edit a student you don't own |

**A note on how this activity works:** you won't find complete, working
code to copy anywhere below. You'll find goals, hints, and a way to check
yourself. Figuring out the exact syntax — from documentation, from what
you already know, sometimes by getting it wrong first — is genuinely part
of the task, not a step being skipped.

---

## Part 1 — OpenAPI & Swagger

### Task 1.1 — Get your own docs running at `/api/docs/`

Follow these steps in order. Each one tells you *what* to do — you work
out the exact syntax.

1. **Install the package** that generates OpenAPI documentation from your
   existing DRF code, and add it to `INSTALLED_APPS`.
2. **Add the one required `REST_FRAMEWORK` setting**, pointing at the
   package's schema class.
3. **Add two new URLs**: one that serves the raw schema, one that serves
   the actual browsable docs page. The package provides a view class for
   each — find both.
4. **Restart your server and visit `/api/docs/`.**

**Hint:** the package is DRF's own officially recommended tool for this.
If you're stuck on exact names, its own README is the right place to
look — reading a real package's documentation under a bit of pressure is
a genuine, normal skill, not cheating.

**Check yourself:** open `/api/docs/` in your browser. You should see
every action on `StudentViewSet`, listed automatically, without you
writing a word of documentation by hand.

### Task 1.2 — Answer these using only your own docs

Open `/api/docs/`, find the `POST /students/` endpoint, and answer:

1. What fields does the request body actually expect?
2. What status code does a successful creation return?
3. What status code does a validation failure return?

Now make one real change: edit `StudentSerializer`'s `mark` field to use a
different `max_value`, and refresh `/api/docs/`.

4. What changed on the page — and did you edit the documentation yourself
   to make that happen?

---

## Part 2 — Postman Collection

### Task 2.1 — Build 3 requests, matching DOC-001/002/003

| Request | Method | Body | Expected result |
|---|---|---|---|
| **DOC-001** | GET `/students/` | — | `200 OK` |
| **DOC-002** | POST `/students/` | a mark that's genuinely out of range | `400 Bad Request` |
| **DOC-003** | PATCH `/students/<id>/` | on a student you don't own | `403 Forbidden` |

You decide the exact body and the exact student id — as long as the
result genuinely matches the table. Save your auth token **once, at the
collection level**, not on each individual request.

**Check yourself:** actually send all three. Confirm you get the real
status codes above — not just that the request saved without errors.

### Task 2.2 — Name them properly

Rename each request to something a stranger could understand without
asking you. "Request 2" tells nobody anything.

---

## Part 3 — DRF APIClient Tests

### Task 3.1 — Set up your test file

Follow these steps in order. Each one tells you *what* to create — you
work out the exact syntax.

1. **Create `student_app/tests.py`**, importing what you'll need:
   `APITestCase`, `status`, your `Student`/`ClassGroup` models, and
   Django's `User` model.
2. **Create a test class** inheriting from `APITestCase`.
3. **Add the one method Django's test framework calls automatically,
   before every single test in the class.** What's it called? (Same name
   in most testing frameworks you'll ever meet, in any language.)
4. **Inside that method, create, in order:**
   - one class group
   - two separate users — DOC-003 specifically needs a student owned by
     one user, and a *different* user attempting to edit it
   - one student, owned by the first user

**Hints:**

- Creating a class group and a student is plain ORM —
  `Model.objects.create(...)`, the same as always.
- Creating a user safely means *not* using plain `.create()` — which
  method did you learn for this back in Module 2, and why does it
  matter?

**Check yourself:** every test method from here on can reference `self.group`,
`self.owner`, `self.other_user`, and `self.student` without you creating
them again — if you find yourself repeating setup inside an individual
test method, it belongs here instead.

### Task 3.2 — Write DOC-001

```python
    def test_DOC_001_list_students_returns_200(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get('/students/')
        self.assertEqual(____________, status.HTTP_200_OK)
```

Fill in the blank. Ask yourself: which real attribute on `response`
actually holds the status code?

### Task 3.3 — Write DOC-002 yourself, from nothing

No scaffold this time. Write a test method that:
- Authenticates as `self.owner`
- POSTs to `/students/` with a mark you already know is invalid
- Asserts the response's status code equals the correct `4xx` status

Work out the exact method calls yourself, based on DOC-001 and what
you've built in earlier sessions.

### Task 3.4 — Write DOC-003 yourself, from nothing

This one directly tests `IsOwnerOrReadOnly`. Write a test method that:
- Authenticates as a user who does **not** own `self.student`
- Attempts to PATCH that student's `mark`
- Asserts the response's status code equals the correct status for
  "forbidden"

**Check yourself:** run `python manage.py test student_app`. You're
looking for `Ran 3 tests` and `OK`, with nothing listed under `FAILED`.
If you see a failure, read the actual error message before changing
anything — it names the exact line and the exact mismatch.

---

## Part 4 — Prove It, Then Break It

### Task 4.1 — Break DOC-003 on purpose

Temporarily change `StudentViewSet.permission_classes` so that
`IsOwnerOrReadOnly` is no longer applied. Run
`python manage.py test student_app` again.

**Check yourself:** DOC-003 should now fail. Read the real
`AssertionError` line in the output — it will show you the two status
codes it compared.

**Now restore your permission_classes**, and confirm all 3 tests pass
again before moving on. Don't skip this — leaving it broken defeats the
point.

### Task 4.2 — Answer honestly, from what you just saw

1. If you'd only had your Postman collection from Part 2, and never
   re-opened it this afternoon, would it have caught this specific break
   on its own? Why or why not?
2. Would your Swagger docs have caught it?
3. Which of today's three tools was the *only* one that caught this
   automatically, with nobody remembering to manually check anything?

---

## How You'll Know You're Done

- [ ] `/api/docs/` shows every `StudentViewSet` action, correctly, and you
      can explain what you'd have to do if you wanted a field's
      description to change.
- [ ] Your Postman collection has 3 clearly-named requests, and you've
      actually sent all three and read the real responses.
- [ ] You wrote DOC-002 and DOC-003 yourself, with no scaffold, and
      `python manage.py test student_app` shows `Ran 3 tests` and `OK`.
- [ ] You broke DOC-003 on purpose, read the real failure message, then
      restored it and confirmed all 3 tests pass again.
- [ ] You can answer, out loud and unprompted, why Postman and Swagger
      wouldn't have caught the break, but the test did.

## Submitting

Submit: a screenshot of your `/api/docs/` page, your exported Postman
collection (`.json`), your final `tests.py`, and one sentence answering
Task 4.2's third question.

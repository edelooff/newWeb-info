#!/usr/bin/python
"""Request handlers for the newWeb example info application."""

# Standard modules
import base64
import json
import logging
import os
import time

# uWeb modules
import newweb
from newweb.pagemaker import login

__version__ = '0.1.0'


class PageMaker(login.LoginMixin, login.OpenIdMixin, newweb.DebuggingPageMaker):
  """Holds all the html generators for the webapp

  Each page as a separate method.
  """
  def CommonBlocks(self, page_id):
    """Returns the common header and footer blocks for this project."""
    return {'header': self.parser.Parse('header.html', page_id=page_id),
            'footer': self.parser.Parse(
                'footer.html',
                year=time.strftime('%Y'),
                version=newweb.__version__)}

  def CustomCookie(self):
    """Sets a cookie, and redirects the user to the index page.

    This way, the cookie will be visible when the user posts the form.
    """
    self.req.AddCookie(self.post.getfirst('nw_cookie_name'),
                       self.post.getfirst('nw_cookie_value', 'default'),
                       path=self.post.getfirst('nw_cookie_path'),
                       max_age=self.post.getfirst('nw_cookie_max_age', 60))
    # We send a 303 instead of a 307 because the latter would repeat the POST.
    # This would trigger a redirect loop, which is a bad bad thing :-)

    #XXX ImmediateResponse drops the current response we're making, thereby
    # destroying any cookies we're setting :(
    #raise uweb.ImmediateResponse(uweb.Redirect('/', httpcode=303))

  def Index(self, _path):
    """Returns the index.html template"""
    if 'nw_cookie_name' in self.post:
      self.CustomCookie()
    return self.parser.Parse(
        'index.html',
        method=self.req.env['REQUEST_METHOD'],
        query=self.get,
        postvars=self.post,
        cookies=self.cookies,
        headers=self.req.headers,
        env=self.req.env,
        **self.CommonBlocks('main'))

  def Json(self):
    """Returns a JSON response with the form data, or just the project name."""
    if self.post:
      data = dict((key, self.post.getfirst(key)) for key in self.post)
    else:
      data = {'name': u'newWeb', 'version': newweb.__version__}
    self.req.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache, must-revalidate'})
    self.req.response.content_type = 'application/json'
    return json.dumps(data, sort_keys=True, indent=4)

  @staticmethod
  def MakeFail():
    """Triggers a HTTP 500 Internal Server Error in uWeb.

    This is a demonstration of the (limited) debugging facilities in uWeb.
    A small stack of calls is created, the last of which raises an error.
    The resulting stack trace and a short introductory message is returned to
    the browser, tagged with a HTTP response code 500.
    """
    def _Processor(function):
      """Uses the given `function` to process the string literal 'foo' with."""
      function('foo')

    def _MakeInteger(numeric_string):
      """Returns the integer value of a numeric string using int()."""
      return int(numeric_string)

    return _Processor(_MakeInteger)

  def NonWordCatchall(self, path):
    """Returns a simple page with a byte-view of the sent request.

    This result is triggered when the path contained non-word Unicode characters
    or a byte-stream that could not be converted to Unicode.
    """
    text = ('You tried to open a page with either invalid UTF8 in it, or'
            'another sequence that did not match the route regex (word chars + '
            'dashes, underscores and slashes. Your request path: %r' % path)
    return self.parser.Parse(
        'freetext.html',
        title=u'Underdark \u2665 Unicode',
        message=text,
        **self.CommonBlocks('uweb'))

  def Text(self):
    """Returns a page with data in text/plain.

    To return a different content type, the returned object must be a Page,
    where the `content_type` argument can be set to any desired mimetype.
    """
    self.req.response.content_type = 'text/plain'
    return """
        <h1>This is a text-only page.</h1>

        Linebreaks and leading whitespace are honored.
        <strong>HTML tags do nothing, as demonstrated above<strong>.
        """

  @staticmethod
  def Redirect(location):
    """Generates a temporary redirect to the given location.

    Returns a HTTP 303 (See Other) redirect which tells the browser that the
    requested document is at the given location and that any POST performed
    should not be performed again. The request method must be HEAD or GET.
    """
    return newweb.Redirect(location, httpcode=303)

  def FourOhFour(self, path):
    """The request could not be fulfilled, this returns a 404."""
    self.req.response.httpcode = 404
    return self.parser.Parse(
        '404.html', path=path, **self.CommonBlocks('http404'))

  def InternalServerError(self, *exc_info):
    """Returns a HTTP 500 page, since the request failed elsewhere."""
    if ('debug' in self.req.env['QUERY_STRING'].lower() or
        'openid' in self.req.path.lower()):
      # Returns the default HTTP 500 handler result. For this class, since we
      # subclassed DebuggingPageMaker, it has all sorts of debug info.
      return super(PageMaker, self).InternalServerError(*exc_info)
    else:
      # Return our custom styled HTTP 500 handler instead, this is what you'll
      # want to serve during production; the debugging one gives too much info.
      path = self.req.path
      logging.warning(
          'Execution of %r triggered an exception', path, exc_info=exc_info)
      self.req.response.httpcode = 500
      return self.parser.Parse(
          '500.html', path=path, **self.CommonBlocks('http500'))

  # ############################################################################
  # OpenID result handlers.
  #
  def OpenIdProviderBadLink(self, err_obj):
    return self.parser.Parse(
        'freetext.html',
        title='Bad OpenID Provider URL',
        message=err_obj,
        **self.CommonBlocks('uweb'))

  def OpenIdProviderError(self, err_obj):
    message = 'The OpenID provider did not respond as expected: %r' % err_obj
    return self.parser.Parse(
        'freetext.html',
        title='Bad OpenID Provider',
        message=message,
        **self.CommonBlocks('uweb'))

  def OpenIdAuthCancel(self, err_obj):
    return self.parser.Parse(
        'freetext.html',
        title='OpenID Authentication canceled by user',
        message=err_obj,
        **self.CommonBlocks('uweb'))

  def OpenIdAuthFailure(self, err_obj):
    return self.parser.Parse(
        'freetext.html',
        title='OpenID Authentication failed',
        message=err_obj,
        **self.CommonBlocks('uweb'))

  def OpenIdAuthSuccess(self, auth_dict):
    message = 'Some authentication info:\n\n%s' % (
        '\n'.join('* %s = %r' % pair for pair in sorted(auth_dict.items())))
    session_id = base64.urlsafe_b64encode(os.urandom(30))
    self.req.AddCookie('FirstMinuteLogin', 'True', max_age=60)
    self.req.AddCookie('OpenIDSession', session_id, max_age=3600)
    return self.parser.Parse(
        'freetext.html',
        title='OpenID Authentication successful!',
        message=message,
        **self.CommonBlocks('uweb'))

  # ############################################################################
  # Underdark Login Framework result handlers.
  #
  def _ULF_Failure(self, secure):
    return self.parser.Parse(
        'freetext.html',
        title='ULF authentication failed',
        message='The secure mode was %r.' % secure,
        **self.CommonBlocks('uweb'))

  def _ULF_Success(self, secure):
    return self.parser.Parse(
        'freetext.html',
        title='ULF authentication successful!',
        message='The secure mode was %r.' % secure,
        **self.CommonBlocks('uweb'))

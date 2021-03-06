// Copyright 2019 Workiva Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import 'package:codemod/codemod.dart';
import 'package:source_span/source_span.dart';

/// Suggestor that wraps an existing suggestor and hides patches that are
/// ignored via a `// orcm_ignore` comment.
///
/// Any patch that is suggested by the given suggestor that starts on a line
/// with the ignore comment or on a line immediately after a line with the
/// ignore comment will be ignored. All other patches will be re-yielded via
/// [generatePatches].
class Ignoreable implements Suggestor {
  static RegExp _ignoreRegex =
      RegExp(r'//[ ]*orcm_ignore[ ]*$', multiLine: true);

  final Suggestor _suggestor;

  Ignoreable(Suggestor suggestor) : _suggestor = suggestor;

  @override
  Iterable<Patch> generatePatches(SourceFile sourceFile) sync* {
    final ignoreLines = _ignoreRegex
        .allMatches(sourceFile.getText(0))
        .map((match) => sourceFile.getLine(match.start));

    yield* _suggestor
        .generatePatches(sourceFile)
        // Skip patches that start on a line (or on a line immediately after a
        // line) with an `// orcm_ignore` comment.
        .where((patch) =>
            !ignoreLines.contains(patch.startLine) &&
            !ignoreLines.contains(patch.startLine - 1));
  }

  @override
  bool shouldSkip(String sourceFileContents) =>
      _suggestor.shouldSkip(sourceFileContents);
}

from ..context import props_and_state_classes
from .util import CodemodPatchTestCase

import codemod
import mock
import re
import unittest


class TestPropsAndStateClassesAccompanyingPublicClassSuggestor(CodemodPatchTestCase):

    @property
    def suggestor(self):
        return props_and_state_classes.props_and_state_classes_accompanying_public_class_suggestor

    def test_empty(self):
        self.suggest('')
        self.assert_no_patches_suggested()

    def test_no_match(self):
        self.suggest('''library foo;

@PropsMixin()
class FooPropsMixin implements UiProps {
    String value;
}
''')
        self.assert_no_patches_suggested()

    def test_props(self):
        self.suggest('''library foo;

@Props()
class FooProps extends UiProps {
    String prop1;

    bool prop2;
}''')
        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=8,
            end_line_number=8,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'class FooProps extends _$FooProps with _$FooPropsAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const PropsMeta meta = $metaForFooProps;\n',
                '}\n',
            ],
        ))

    def test_abstract_props(self):
        self.suggest('''library foo;

@AbstractProps()
abstract class FooProps extends UiProps {
    String prop1;

    bool prop2;
}''')
        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=8,
            end_line_number=8,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'abstract class FooProps extends _$FooProps with _$FooPropsAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const PropsMeta meta = $metaForFooProps;\n',
                '}\n',
            ],
        ))

    def test_state(self):
        self.suggest('''library foo;

@State()
class FooState extends UiState {
    String state1;

    bool state2;
}''')
        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=8,
            end_line_number=8,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'class FooState extends _$FooState with _$FooStateAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const StateMeta meta = $metaForFooState;\n',
                '}\n',
            ],
        ))

    def test_abstract_state(self):
        self.suggest('''library foo;

@AbstractState()
abstract class FooState extends UiState {
    String state1;

    bool state2;
}''')
        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=8,
            end_line_number=8,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'abstract class FooState extends _$FooState with _$FooStateAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const StateMeta meta = $metaForFooState;\n',
                '}\n',
            ],
        ))

    def test_annotation_with_arg(self):
        self.suggest('''library foo;

@Props(keyNamespace: 'test')
class FooProps extends UiProps {
    String prop1;

    bool prop2;
}''')
        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=8,
            end_line_number=8,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'class FooProps extends _$FooProps with _$FooPropsAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const PropsMeta meta = $metaForFooProps;\n',
                '}\n',
            ],
        ))

    def test_multiple_annotations(self):
        self.suggest('''library foo;

@Props()
@Deprecated('3.0.0')
class FooProps extends UiProps {
    String prop1;

    bool prop2;
}''')
        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=9,
            end_line_number=9,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'class FooProps extends _$FooProps with _$FooPropsAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const PropsMeta meta = $metaForFooProps;\n',
                '}\n',
            ],
        ))
    
    def test_private_class(self):
        self.suggest('''library foo;

@Props()
class _FooProps extends UiProps {
    String prop1;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=6,
            end_line_number=6,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'class _FooProps extends _$FooProps with _$FooPropsAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const PropsMeta meta = _$metaForFooProps;\n',
                '}\n',
            ],
        ))

# TODO: generics not currently supported
#     def test_generics(self):
#         self.suggest('''library foo;

# @Props()
# class FooProps<T extends Iterable, Foo<U>> extends UiProps {
#     String prop1;

#     bool prop2;
# }''')
#         self.assert_num_patches_suggested(1)
#         self.assert_patch_suggested(codemod.Patch(
#             start_line_number=8,
#             end_line_number=8,
#             new_lines=[
#                 '\n',
#                 '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
#                 '// ignore: mixin_of_non_class, undefined_class\n',
#                 'class FooProps<T extends Iterable, Foo<U>> extends _$FooProps with _$FooPropsAccessorsMixin {\n',
#                 '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
#                 '  static const PropsMeta meta = $metaForFooProps;\n',
#                 '}\n',
#             ],
#         ))

    def test_already_renamed_but_missing_accompanying_class(self):
        self.suggest('''library foo;

@Props()
class _$FooProps extends UiProps {
    String prop1;

    bool prop2;
}''')
        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=8,
            end_line_number=8,
            new_lines=[
                '\n',
                '// AF-3369 This will be removed once the transition to Dart 2 is complete.\n',
                '// ignore: mixin_of_non_class, undefined_class\n',
                'class FooProps extends _$FooProps with _$FooPropsAccessorsMixin {\n',
                '  // ignore: undefined_identifier, undefined_class, const_initialized_with_non_constant_value\n',
                '  static const PropsMeta meta = $metaForFooProps;\n',
                '}\n',
            ],
        ))

    def test_already_added(self):
        self.suggest('''library foo;

@Props()
class _$FooProps extends UiProps {
    String prop1;

    bool prop2;
}

class FooProps extends _$FooProps with _$FooPropsAccessorsMixin {}''')
        self.assert_no_patches_suggested()


class TestPropsAndStateClassesRenameSuggestor(CodemodPatchTestCase):
    @property
    def suggestor(self):
        return props_and_state_classes.props_and_state_classes_rename_suggestor

    def test_empty(self):
        self.suggest('')
        self.assert_no_patches_suggested()

    def test_no_match(self):
        self.suggest('''library foo;

@PropsMixin()
class FooPropsMixin implements UiProps {
    String value;
}
''')
        self.assert_no_patches_suggested()

    def test_props(self):
        self.suggest('''library foo;

@Props()
class FooProps extends UiProps {
    String foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@Props()\n',
                'class _$FooProps extends UiProps {\n',
            ],
        ))

    def test_state(self):
        self.suggest('''library foo;

@State()
class FooState extends UiState {
    String foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@State()\n',
                'class _$FooState extends UiState {\n',
            ],
        ))

    def test_abstract_props(self):
        self.suggest('''library foo;

@AbstractProps()
abstract class AbstractFooProps extends UiProps {
    String get foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@AbstractProps()\n',
                'abstract class _$AbstractFooProps extends UiProps {\n',
            ],
        ))

    def test_abstract_state(self):
        self.suggest('''library foo;

@AbstractState()
abstract class AbstractFooState extends UiState {
    String get foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@AbstractState()\n',
                'abstract class _$AbstractFooState extends UiState {\n',
            ],
        ))

    def test_empty_class_body(self):
        self.suggest('''library foo;

@Props()
class FooProps extends UiProps {}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@Props()\n',
                'class _$FooProps extends UiProps {}\n',
            ],
        ))

    def test_extra_annotation(self):
        self.suggest('''library foo;

@Props()
@Deprecated("3.0.0")
class FooProps extends UiProps {
    String foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=5,
            new_lines=[
                '@Props()\n',
                '@Deprecated("3.0.0")\n',
                'class _$FooProps extends UiProps {\n',
            ],
        ))

    def test_annotation_args(self):
        self.suggest('''library foo;

@Props(keyNamespace: "bar")
class FooProps extends UiProps {
    String foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@Props(keyNamespace: "bar")\n',
                'class _$FooProps extends UiProps {\n',
            ],
        ))

    def test_private(self):
        self.suggest('''library foo;

@Props()
class _PrivateFooProps extends UiProps {
    String foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@Props()\n',
                'class _$PrivateFooProps extends UiProps {\n',
            ],
        ))

    def test_special_chars(self):
        self.suggest('''library foo;

@Props()
class Foo_Props extends UiProps {
    String foo;
}''')

        self.assert_num_patches_suggested(1)
        self.assert_patch_suggested(codemod.Patch(
            start_line_number=2,
            end_line_number=4,
            new_lines=[
                '@Props()\n',
                'class _$Foo_Props extends UiProps {\n',
            ],
        ))
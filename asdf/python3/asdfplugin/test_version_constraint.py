import unittest
import io
import version_constraint


class Test_VersionConstraint(unittest.TestCase):
    def test_test_version_gt(self):
        c = version_constraint.VersionConstraint([(">", "1.2.3")])
        self.assertTrue(c.test_version("1.2.4"))
        self.assertTrue(c.test_version("1.3.0"))
        self.assertTrue(c.test_version("1.3"))
        self.assertTrue(c.test_version("2"))
        self.assertTrue(c.test_version("2.0.0"))
        self.assertFalse(c.test_version("1.2.3"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertFalse(c.test_version("0.0.1"))
        self.assertFalse(c.test_version("1.2"))
        self.assertFalse(c.test_version("1"))

    def test_test_version_lt(self):
        c = version_constraint.VersionConstraint([("<", "1.2.3")])
        self.assertTrue(c.test_version("1.2.2"))
        self.assertTrue(c.test_version("1.1.0"))
        self.assertTrue(c.test_version("0.0.1"))
        self.assertTrue(c.test_version("1.2"))
        self.assertTrue(c.test_version("1"))
        self.assertFalse(c.test_version("1.2.3"))
        self.assertFalse(c.test_version("1.2.4"))
        self.assertFalse(c.test_version("1.3.0"))
        self.assertFalse(c.test_version("1.3"))
        self.assertFalse(c.test_version("2"))

    def test_test_version_ge(self):
        c = version_constraint.VersionConstraint([(">=", "1.2.3")])
        self.assertTrue(c.test_version("1.2.4"))
        self.assertTrue(c.test_version("1.3.0"))
        self.assertTrue(c.test_version("1.3"))
        self.assertTrue(c.test_version("2"))
        self.assertTrue(c.test_version("2.0.0"))
        self.assertTrue(c.test_version("1.2.3"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertFalse(c.test_version("0.0.1"))
        self.assertFalse(c.test_version("1.2"))
        self.assertFalse(c.test_version("1"))

    def test_test_version_le(self):
        c = version_constraint.VersionConstraint([("<=", "1.2.3")])
        self.assertTrue(c.test_version("1.2.2"))
        self.assertTrue(c.test_version("1.1.0"))
        self.assertTrue(c.test_version("0.0.1"))
        self.assertTrue(c.test_version("1.2"))
        self.assertTrue(c.test_version("1"))
        self.assertTrue(c.test_version("1.2.3"))
        self.assertFalse(c.test_version("1.2.4"))
        self.assertFalse(c.test_version("1.3.0"))
        self.assertFalse(c.test_version("1.3"))
        self.assertFalse(c.test_version("2"))

    def test_test_version_eq(self):
        c = version_constraint.VersionConstraint([("=", "1.2.3")])
        self.assertTrue(c.test_version("1.2.3"))
        self.assertFalse(c.test_version("1.2.4"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("1.2"))
        self.assertFalse(c.test_version("1"))

    def test_test_version_eq_minor(self):
        c = version_constraint.VersionConstraint([("=", "1.2.0")])
        self.assertTrue(c.test_version("1.2.0"))
        self.assertTrue(c.test_version("1.2"))
        self.assertFalse(c.test_version("1.2.4"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("1"))

    def test_test_version_ne(self):
        c = version_constraint.VersionConstraint([("!=", "1.2.3")])
        self.assertFalse(c.test_version("1.2.3"))
        self.assertTrue(c.test_version("1.2.4"))
        self.assertTrue(c.test_version("1.2.2"))
        self.assertTrue(c.test_version("2"))
        self.assertTrue(c.test_version("2"))
        self.assertTrue(c.test_version("1.2"))
        self.assertTrue(c.test_version("1"))

    def test_test_version_ne_minor(self):
        c = version_constraint.VersionConstraint([("!=", "1.2.0")])
        self.assertFalse(c.test_version("1.2.0"))
        self.assertFalse(c.test_version("1.2"))
        self.assertTrue(c.test_version("1.2.4"))
        self.assertTrue(c.test_version("1.2.2"))
        self.assertTrue(c.test_version("2"))
        self.assertTrue(c.test_version("2"))
        self.assertTrue(c.test_version("1"))

    def test_test_version_ge_minor(self):
        c = version_constraint.VersionConstraint([("~>", "1.2.3")])
        self.assertTrue(c.test_version("1.2.3"))
        self.assertTrue(c.test_version("1.2.4"))
        self.assertTrue(c.test_version("1.2.10"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertFalse(c.test_version("1.3.0"))
        self.assertFalse(c.test_version("1.3"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("0.0.1"))
        self.assertFalse(c.test_version("1.2"))
        self.assertFalse(c.test_version("1"))

    def test_test_version_ge_minor_equivalent(self):
        c = version_constraint.VersionConstraint([(">=", "1.2.3"), ("<", "1.3.0")])
        self.assertTrue(c.test_version("1.2.3"))
        self.assertTrue(c.test_version("1.2.4"))
        self.assertTrue(c.test_version("1.2.10"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertFalse(c.test_version("1.3.0"))
        self.assertFalse(c.test_version("1.3"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("0.0.1"))
        self.assertFalse(c.test_version("1.2"))
        self.assertFalse(c.test_version("1"))

    def test_test_version_complex(self):
        c = version_constraint.VersionConstraint(
            [(">=", "1.2.3"), ("<=", "3"), ("!=", "2.5"), ("!=", "1.2.4")]
        )
        self.assertFalse(c.test_version("0.1.2"))
        self.assertFalse(c.test_version("1"))
        self.assertFalse(c.test_version("1.2"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertTrue(c.test_version("1.2.3"))
        self.assertFalse(c.test_version("1.2.4"))
        self.assertTrue(c.test_version("1.2.5"))
        self.assertTrue(c.test_version("2.4.9"))
        self.assertFalse(c.test_version("2.5"))
        self.assertFalse(c.test_version("2.5.0"))
        self.assertTrue(c.test_version("2.5.1"))
        self.assertTrue(c.test_version("2.5.2"))
        self.assertTrue(c.test_version("2.9.1"))
        self.assertTrue(c.test_version("2.15.0"))
        self.assertTrue(c.test_version("3"))
        self.assertTrue(c.test_version("3.0"))
        self.assertTrue(c.test_version("3.0.0"))
        self.assertFalse(c.test_version("3.0.1"))
        self.assertFalse(c.test_version("3.1"))
        self.assertFalse(c.test_version("3.1.0"))

    def test_test_version_complex2(self):
        c = version_constraint.VersionConstraint(
            [(">=", "1.2.3"), ("<=", "3"), ("!=", "2.5"), ("=", "1.2.4")]
        )
        self.assertFalse(c.test_version("0.1.2"))
        self.assertFalse(c.test_version("1"))
        self.assertFalse(c.test_version("1.2"))
        self.assertFalse(c.test_version("1.2.2"))
        self.assertFalse(c.test_version("1.2.3"))
        self.assertTrue(c.test_version("1.2.4"))
        self.assertFalse(c.test_version("1.2.5"))
        self.assertFalse(c.test_version("2.4.9"))
        self.assertFalse(c.test_version("2.5"))
        self.assertFalse(c.test_version("2.5.0"))
        self.assertFalse(c.test_version("2.5.1"))
        self.assertFalse(c.test_version("2.5.2"))
        self.assertFalse(c.test_version("2.9.1"))
        self.assertFalse(c.test_version("2.15.0"))
        self.assertFalse(c.test_version("3"))
        self.assertFalse(c.test_version("3.0"))
        self.assertFalse(c.test_version("3.0.0"))
        self.assertFalse(c.test_version("3.0.1"))
        self.assertFalse(c.test_version("3.1"))
        self.assertFalse(c.test_version("3.1.0"))

    def test_filter_versions_range(self):
        c = version_constraint.VersionConstraint([(">=", "1.2.3"), ("<=", "3")])
        self.assertListEqual(
            c.filter_versions(
                ["1.2.2", "1.2.3", "1.2.4", "2", "2.9", "3.0.0", "3.0.1", "4.5.1"]
            ),
            ["1.2.3", "1.2.4", "2", "2.9", "3.0.0"],
        )

    def test_filter_versions_ne(self):
        c = version_constraint.VersionConstraint([("!=", "1.2.3"), ("!=", "3")])
        self.assertListEqual(
            c.filter_versions(
                ["1.2.2", "1.2.3", "1.2.4", "2", "2.9", "3.0.0", "3.0.1", "4.5.1"]
            ),
            ["1.2.2", "1.2.4", "2", "2.9", "3.0.1", "4.5.1"],
        )

    def test_filter_versions_eq(self):
        c = version_constraint.VersionConstraint([("=", "1.2.3")])
        self.assertListEqual(
            c.filter_versions(
                ["1.2.2", "1.2.3", "1.2.4", "2", "2.9", "3.0.0", "3.0.1", "4.5.1"]
            ),
            ["1.2.3"],
        )

    def test_latest_matching_range(self):
        c = version_constraint.VersionConstraint([(">=", "1.2.3"), ("<=", "3")])
        self.assertEqual(
            c.latest_matching(
                ["1.2.2", "1.2.3", "1.2.4", "2", "2.9", "3.0.0", "3.0.1", "4.5.1"]
            ),
            "3.0.0",
        )

    def test_latest_matching_eq(self):
        c = version_constraint.VersionConstraint([("=", "1.2.3")])
        self.assertEqual(
            c.latest_matching(
                ["1.2.2", "1.2.3", "1.2.4", "2", "2.9", "3.0.0", "3.0.1", "4.5.1"]
            ),
            "1.2.3",
        )

    def test_latest_matching_none(self):
        c = version_constraint.VersionConstraint([("=", "1.2.3")])
        self.assertIsNone(
            c.latest_matching(["1.2.2", "1.2.4", "2", "2.9", "3.0.0", "3.0.1", "4.5.1"])
        )

    def test_constraint_from_tf_string(self):
        c = version_constraint.constraint_from_tf_string(">= 1.10.5, < 1.12, != 1.11.2")
        self.assertTrue(c.test_version("1.10.5"))
        self.assertTrue(c.test_version("1.10.6"))
        self.assertTrue(c.test_version("1.11.1"))
        self.assertTrue(c.test_version("1.11.3"))
        self.assertTrue(c.test_version("1.11"))
        self.assertTrue(c.test_version("1.11.99"))
        self.assertFalse(c.test_version("1"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("1.12"))
        self.assertFalse(c.test_version("1.12.0"))
        self.assertFalse(c.test_version("1.11.2"))
        self.assertFalse(c.test_version("1.13"))

    def test_constraint_from_tf_eq(self):
        c = version_constraint.constraint_from_tf_string(">= 1.10.5, < 1.12, 1.11.2")
        self.assertFalse(c.test_version("1.10.5"))
        self.assertFalse(c.test_version("1.10.6"))
        self.assertFalse(c.test_version("1.11.1"))
        self.assertFalse(c.test_version("1.11.3"))
        self.assertFalse(c.test_version("1.11"))
        self.assertFalse(c.test_version("1.11.99"))
        self.assertFalse(c.test_version("1"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("1.12"))
        self.assertFalse(c.test_version("1.12.0"))
        self.assertTrue(c.test_version("1.11.2"))
        self.assertFalse(c.test_version("1.13"))

    def test_constraint_from_tf_gt_minor(self):
        c = version_constraint.constraint_from_tf_string("~> 1.10.5")
        self.assertTrue(c.test_version("1.10.5"))
        self.assertTrue(c.test_version("1.10.6"))
        self.assertFalse(c.test_version("1.11.1"))
        self.assertFalse(c.test_version("1.11"))
        self.assertFalse(c.test_version("1"))
        self.assertFalse(c.test_version("2"))
        self.assertFalse(c.test_version("1.10.4"))
        self.assertFalse(c.test_version("1.12.0"))
        self.assertFalse(c.test_version("1.10"))

    def test_constraint_from_tf_file_none(self):
        c = version_constraint.constraint_from_tf_file(
            io.StringIO("some text without the necessary content")
        )
        self.assertIsNone(c)

    def test_constraint_from_tf_file(self):
        c = version_constraint.constraint_from_tf_file(
            io.StringIO(
                """
terraform {
  required_providers {
    sops = {
      source = "carlpett/sops"
    }
  }
  required_version = ">= 1.10.5, < 1.12, != 1.11.2"
}
"""
            )
        )
        self.assertIsNot(c, None)
        self.assertEqual(str(c), ">= 1.10.5, < 1.12, != 1.11.2")

    def test_stringify(self):
        in_str = ">= 1.10.5, < 1.12, != 1.11.2"
        c = version_constraint.constraint_from_tf_string(in_str)
        out_str = str(c)
        self.assertEqual(in_str, out_str)


if __name__ == "__main__":
    unittest.main()
